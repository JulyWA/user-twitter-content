#!/usr/bin/env python3
"""
Archive Twitter/X timelines from RapidAPI's twitter154 host.

The script keeps the raw API payloads and also writes normalized JSONL plus a
small clean JSON format that matches the existing kol-scorer source data.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any


DEFAULT_HOST = "twitter154.p.rapidapi.com"
DEFAULT_OUTPUT_DIR = Path("data/users")
DEFAULT_LIMIT = 20
DEFAULT_SLEEP_SECONDS = 2.0
DEFAULT_MAX_PAGES = 0


class Twitter154Client:
    def __init__(
        self,
        api_key: str,
        host: str = DEFAULT_HOST,
        timeout: int = 20,
        retries: int = 3,
    ) -> None:
        self.host = host
        self.timeout = timeout
        self.retries = retries
        import requests

        self.requests = requests
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": host,
                "Content-Type": "application/json",
            }
        )

    def get_first_page(
        self,
        username: str,
        limit: int,
        include_replies: bool,
        include_pinned: bool,
    ) -> dict[str, Any]:
        url = f"https://{self.host}/user/tweets"
        params = {
            "username": username,
            "limit": limit,
            "include_replies": str(include_replies).lower(),
            "include_pinned": str(include_pinned).lower(),
        }
        return self._request("GET", url, params=params)

    def get_continuation_page(
        self,
        user_id: str,
        continuation_token: str,
        limit: int,
    ) -> dict[str, Any]:
        url = f"https://{self.host}/user/tweets/continuation"
        payload = {
            "user_id": user_id,
            "continuation_token": continuation_token,
            "limit": limit,
        }
        return self._request("POST", url, json=payload)

    def _request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs,
                )
                if response.status_code in {429, 500, 502, 503, 504}:
                    delay = min(60, 2**attempt)
                    print(
                        f"    transient HTTP {response.status_code}; "
                        f"retrying in {delay}s ({attempt}/{self.retries})"
                    )
                    time.sleep(delay)
                    continue
                response.raise_for_status()
                return response.json()
            except (self.requests.RequestException, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt == self.retries:
                    break
                delay = min(60, 2**attempt)
                print(f"    request failed; retrying in {delay}s ({attempt}/{self.retries})")
                time.sleep(delay)
        raise RuntimeError(f"request failed after {self.retries} attempts: {last_error}")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_twitter_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, IndexError):
        return None


def tweet_sort_key(tweet: dict[str, Any]) -> int:
    value = tweet.get("timestamp")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return 0


def tweet_id(tweet: dict[str, Any]) -> str | None:
    value = tweet.get("tweet_id") or tweet.get("id") or tweet.get("id_str")
    return str(value) if value else None


def dedupe_tweets(tweets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    missing_id: list[dict[str, Any]] = []
    for tweet in tweets:
        tid = tweet_id(tweet)
        if tid:
            by_id[tid] = tweet
        else:
            missing_id.append(tweet)
    merged = list(by_id.values()) + missing_id
    return sorted(merged, key=tweet_sort_key, reverse=True)


def extract_quoted_text(tweet: dict[str, Any]) -> str:
    quoted = tweet.get("quoted_status")
    if isinstance(quoted, dict):
        return str(quoted.get("text") or quoted.get("full_text") or "")
    quoted_id = tweet.get("quoted_status_id")
    return str(quoted_id or "")


def normalize_tweet(tweet: dict[str, Any], username: str) -> dict[str, Any]:
    user = tweet.get("user") if isinstance(tweet.get("user"), dict) else {}
    tid = tweet_id(tweet)
    return {
        "tweet_id": tid,
        "url": f"https://x.com/{username}/status/{tid}" if tid else None,
        "username": username,
        "author_user_id": str(user.get("user_id")) if user.get("user_id") else None,
        "author_name": user.get("name"),
        "created_at": parse_twitter_date(tweet.get("creation_date")),
        "created_at_raw": tweet.get("creation_date"),
        "timestamp": tweet.get("timestamp"),
        "text": tweet.get("text") or tweet.get("full_text") or "",
        "language": tweet.get("language"),
        "favorite_count": tweet.get("favorite_count"),
        "retweet_count": tweet.get("retweet_count"),
        "reply_count": tweet.get("reply_count"),
        "quote_count": tweet.get("quote_count"),
        "bookmark_count": tweet.get("bookmark_count"),
        "views": tweet.get("views"),
        "is_retweet": bool(tweet.get("retweet")),
        "in_reply_to_status_id": tweet.get("in_reply_to_status_id"),
        "conversation_id": tweet.get("conversation_id"),
        "quoted_status_id": tweet.get("quoted_status_id"),
        "quoted_text": extract_quoted_text(tweet),
        "expanded_url": tweet.get("expanded_url"),
        "media_url": tweet.get("media_url"),
        "video_url": tweet.get("video_url"),
        "source": tweet.get("source"),
    }


def clean_tweet(tweet: dict[str, Any]) -> dict[str, Any]:
    created_raw = str(tweet.get("creation_date") or "")
    date = " ".join(created_raw.split()[:4])
    if len(date) > 16:
        date = date[:16]
    return {
        "date": date,
        "text": tweet.get("text") or tweet.get("full_text") or "",
        "quoted": extract_quoted_text(tweet),
        "likes": tweet.get("favorite_count") or 0,
        "views": tweet.get("views") or 0,
    }


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    tmp_path.replace(path)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
    tmp_path.replace(path)


def load_usernames(args: argparse.Namespace) -> list[str]:
    usernames: list[str] = []
    for username in args.usernames:
        usernames.append(username)
    if args.user_file:
        with args.user_file.open("r", encoding="utf-8") as handle:
            for line in handle:
                value = line.strip()
                if value and not value.startswith("#"):
                    usernames.append(value)
    cleaned: list[str] = []
    seen: set[str] = set()
    for username in usernames:
        username = username.strip().lstrip("@")
        if username and username.lower() not in seen:
            cleaned.append(username)
            seen.add(username.lower())
    return cleaned


def infer_user_id(tweets: list[dict[str, Any]]) -> str | None:
    for tweet in tweets:
        user = tweet.get("user")
        if isinstance(user, dict) and user.get("user_id"):
            return str(user["user_id"])
    return None


def archive_username(
    client: Twitter154Client,
    username: str,
    args: argparse.Namespace,
) -> None:
    safe_username = username.lstrip("@")
    user_dir = args.output_dir / safe_username
    raw_path = user_dir / "sources" / "twitter" / "raw" / "tweets_raw.json"
    jsonl_path = user_dir / "sources" / "twitter" / "normalized" / "tweets.jsonl"
    clean_path = user_dir / "sources" / "twitter" / "clean" / "tweets_clean.json"
    checkpoint_path = user_dir / "state" / "twitter_checkpoint.json"

    existing = read_json(raw_path, {})
    existing_tweets = existing.get("tweets", []) if isinstance(existing, dict) else []
    checkpoint = read_json(checkpoint_path, {})

    all_tweets = list(existing_tweets)
    continuation_token = None
    user_id = None
    start_from_checkpoint = (
        args.resume
        and isinstance(checkpoint, dict)
        and checkpoint.get("continuation_token")
        and checkpoint.get("user_id")
        and not args.fresh
    )

    if start_from_checkpoint:
        continuation_token = str(checkpoint["continuation_token"])
        user_id = str(checkpoint["user_id"])
        page = int(checkpoint.get("pages_fetched", 0))
        print(f"@{safe_username}: resuming from checkpoint at page {page + 1}")
    else:
        page = 0
        print(f"@{safe_username}: fetching first page")
        data = client.get_first_page(
            safe_username,
            args.limit,
            args.include_replies,
            args.include_pinned,
        )
        tweets = data.get("results", [])
        if not isinstance(tweets, list):
            tweets = []
        all_tweets.extend(tweets)
        all_tweets = dedupe_tweets(all_tweets)
        user_id = infer_user_id(tweets) or infer_user_id(all_tweets)
        continuation_token = data.get("continuation_token")
        page = 1
        save_outputs(
            safe_username,
            all_tweets,
            page,
            continuation_token,
            user_id,
            args,
            raw_path,
            jsonl_path,
            clean_path,
            checkpoint_path,
        )
        print(f"  page {page}: +{len(tweets)} tweets, total {len(all_tweets)}")

    while continuation_token:
        if args.max_pages and page >= args.max_pages:
            print(f"  reached --max-pages={args.max_pages}; checkpoint kept for resume")
            break
        if not user_id:
            print("  missing user_id; cannot request continuation page")
            break
        time.sleep(args.sleep)
        page += 1
        data = client.get_continuation_page(user_id, continuation_token, args.limit)
        tweets = data.get("results", [])
        if not isinstance(tweets, list) or not tweets:
            continuation_token = None
            print(f"  page {page}: no results; stopping")
            break
        before = len(all_tweets)
        all_tweets.extend(tweets)
        all_tweets = dedupe_tweets(all_tweets)
        added = len(all_tweets) - before
        continuation_token = data.get("continuation_token")
        save_outputs(
            safe_username,
            all_tweets,
            page,
            continuation_token,
            user_id,
            args,
            raw_path,
            jsonl_path,
            clean_path,
            checkpoint_path,
        )
        print(f"  page {page}: +{added} new/{len(tweets)} fetched, total {len(all_tweets)}")

    all_tweets = dedupe_tweets(all_tweets)
    save_outputs(
        safe_username,
        all_tweets,
        page,
        continuation_token,
        user_id,
        args,
        raw_path,
        jsonl_path,
        clean_path,
        checkpoint_path,
    )
    if not continuation_token:
        checkpoint_path.unlink(missing_ok=True)
    print(f"@{safe_username}: archived {len(all_tweets)} unique tweets")
    print(f"  raw   {raw_path}")
    print(f"  jsonl {jsonl_path}")
    print(f"  clean {clean_path}")


def save_outputs(
    username: str,
    tweets: list[dict[str, Any]],
    pages_fetched: int,
    continuation_token: str | None,
    user_id: str | None,
    args: argparse.Namespace,
    raw_path: Path,
    jsonl_path: Path,
    clean_path: Path,
    checkpoint_path: Path,
) -> None:
    normalized = [normalize_tweet(tweet, username) for tweet in tweets]
    raw = {
        "username": username,
        "api_host": args.host,
        "fetched_at": utc_now_iso(),
        "include_replies": args.include_replies,
        "include_pinned": args.include_pinned,
        "pages_fetched": pages_fetched,
        "total": len(tweets),
        "tweets": tweets,
    }
    if tweets:
        raw["newest_timestamp"] = tweet_sort_key(tweets[0])
        raw["oldest_timestamp"] = tweet_sort_key(tweets[-1])
    write_json(raw_path, raw)
    write_jsonl(jsonl_path, normalized)
    write_json(clean_path, [clean_tweet(tweet) for tweet in tweets])
    if continuation_token:
        write_json(
            checkpoint_path,
            {
                "username": username,
                "api_host": args.host,
                "updated_at": utc_now_iso(),
                "pages_fetched": pages_fetched,
                "user_id": user_id,
                "continuation_token": continuation_token,
                "total": len(tweets),
            },
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive Twitter/X timelines through RapidAPI twitter154."
    )
    parser.add_argument("usernames", nargs="*", help="X usernames, with or without @")
    parser.add_argument("--user-file", type=Path, help="Text file with one username per line")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path(".env.local"),
        help="Optional local env file. Values already in the shell take priority.",
    )
    parser.add_argument("--host", default=os.getenv("RAPIDAPI_HOST", DEFAULT_HOST))
    parser.add_argument("--key-env", default="RAPIDAPI_KEY")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="0 means keep paging until the API stops returning continuation tokens.",
    )
    parser.add_argument("--sleep", type=float, default=DEFAULT_SLEEP_SECONDS)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--include-replies", action="store_true")
    parser.add_argument("--include-pinned", action="store_true")
    parser.add_argument("--fresh", action="store_true", help="Ignore checkpoint and start at page 1")
    parser.add_argument(
        "--no-resume",
        dest="resume",
        action="store_false",
        help="Do not continue from a saved checkpoint.",
    )
    parser.set_defaults(resume=True)
    return parser.parse_args(argv)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    load_env_file(args.env_file)
    usernames = load_usernames(args)
    if not usernames:
        print("No usernames provided. Example: archive_twitter_kols.py BTCdayu 0xSunNFT")
        return 2

    api_key = os.getenv(args.key_env)
    if not api_key:
        print(f"Missing {args.key_env}. Set it before running:")
        print(f"  export {args.key_env}='your_rapidapi_key'")
        return 2

    client = Twitter154Client(
        api_key=api_key,
        host=args.host,
        timeout=args.timeout,
        retries=args.retries,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for username in usernames:
        archive_username(client, username, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
