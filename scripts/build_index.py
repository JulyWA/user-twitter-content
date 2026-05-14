#!/usr/bin/env python3
"""
Build cross-user indexes for the curated knowledge layer.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_USERS_DIR = Path("data/users")
DEFAULT_INDEX_DIR = Path("data/index")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


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


def build_indexes(users_dir: Path, index_dir: Path) -> None:
    users: list[dict[str, Any]] = []
    all_knowledge: list[dict[str, Any]] = []
    all_links: list[dict[str, Any]] = []

    for user_dir in sorted(path for path in users_dir.iterdir() if path.is_dir()):
        handle = user_dir.name
        knowledge = read_jsonl(user_dir / "knowledge" / "twitter_knowledge.jsonl")
        links = read_jsonl(user_dir / "knowledge" / "twitter_links.jsonl")
        excluded = read_jsonl(user_dir / "knowledge" / "twitter_excluded.jsonl")
        normalized = read_jsonl(user_dir / "sources" / "twitter" / "normalized" / "tweets.jsonl")

        categories = Counter(category for row in knowledge for category in row.get("categories", []))
        users.append(
            {
                "handle": handle,
                "sources": ["twitter"],
                "twitter": {
                    "normalized_tweets": len(normalized),
                    "knowledge_records": len(knowledge),
                    "link_records": len(links),
                    "excluded_records": len(excluded),
                    "newest": normalized[0].get("created_at") if normalized else None,
                    "oldest": normalized[-1].get("created_at") if normalized else None,
                    "top_categories": categories.most_common(),
                },
                "paths": {
                    "knowledge": f"data/users/{handle}/knowledge/twitter_knowledge.jsonl",
                    "links": f"data/users/{handle}/knowledge/twitter_links.jsonl",
                    "summary": f"data/users/{handle}/knowledge/twitter_summary.md",
                },
            }
        )
        all_knowledge.extend(knowledge)
        all_links.extend(links)

    all_knowledge.sort(key=lambda row: row.get("created_at") or "", reverse=True)
    all_links.sort(key=lambda row: row.get("created_at") or "", reverse=True)

    write_json(index_dir / "users.json", users)
    write_jsonl(index_dir / "twitter_knowledge_all.jsonl", all_knowledge)
    write_jsonl(index_dir / "twitter_links_all.jsonl", all_links)
    print(
        f"indexed {len(users)} users, "
        f"{len(all_knowledge)} knowledge records, {len(all_links)} link records"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build cross-user knowledge indexes.")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR)
    parser.add_argument("--index-dir", type=Path, default=DEFAULT_INDEX_DIR)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.users_dir.exists():
        print(f"No users directory found: {args.users_dir}")
        return 0
    build_indexes(args.users_dir, args.index_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
