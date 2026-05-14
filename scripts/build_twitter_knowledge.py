#!/usr/bin/env python3
"""
Build a research-oriented knowledge layer from archived Twitter/X data.

This is intentionally a transparent heuristic pass. It keeps raw data separate
from the knowledge base so the filter can become stricter or LLM-assisted later
without losing provenance.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_USERS_DIR = Path("data/users")

SIGNAL_RULES: list[tuple[str, int, list[str]]] = [
    (
        "project_thesis",
        4,
        [
            "项目",
            "协议",
            "生态",
            "赛道",
            "行业",
            "龙头",
            "护城河",
            "商业模式",
            "收入",
            "营收",
            "增速",
            "现金流",
            "基本面",
            "估值",
            "市值",
            "FDV",
            "IPO",
            "Pre-IPO",
            "定价",
            "发行",
            "TVL",
            "PMF",
            "代币经济",
            "tokenomics",
            "解锁",
            "回购",
            "费用",
        ],
    ),
    (
        "investment_framework",
        4,
        [
            "框架",
            "逻辑",
            "判断",
            "筛选",
            "标准",
            "复盘",
            "认知",
            "研究",
            "投研",
            "赚钱",
            "本金",
            "长期",
            "赔率",
            "胜率",
            "风险收益比",
            "仓位",
            "建仓",
            "止损",
            "加仓",
        ],
    ),
    (
        "market_cycle",
        3,
        [
            "牛市",
            "熊市",
            "周期",
            "币圈",
            "Crypto",
            "AI",
            "流动性",
            "降息",
            "宏观",
            "行情",
            "轮动",
            "叙事",
            "主线",
            "回调",
            "涨幅",
            "下跌",
            "顶部",
            "底部",
            "突破",
        ],
    ),
    (
        "onchain_strategy",
        3,
        [
            "链上",
            "聪明钱",
            "地址",
            "巨鲸",
            "持仓",
            "筹码",
            "DEX",
            "CEX",
            "上币",
            "meme",
            "MEME",
            "合约地址",
            "pump",
        ],
    ),
    (
        "risk_warning",
        4,
        [
            "风险",
            "陷阱",
            "归零",
            "割",
            "砸盘",
            "出货",
            "跑路",
            "骗局",
            "控盘",
            "解锁",
            "清算",
            "亏损",
            "小心",
            "不要碰",
            "不碰",
        ],
    ),
    (
        "research_source",
        2,
        [
            "研报",
            "报告",
            "数据",
            "图表",
            "白皮书",
            "文章",
            "播客",
            "访谈",
            "thread",
            "长文",
            "链接",
        ],
    ),
    (
        "style_sample",
        1,
        [
            "我认为",
            "我的理解",
            "简单说",
            "本质上",
            "换句话说",
            "一句话",
            "核心是",
        ],
    ),
]

NOISE_KEYWORDS = [
    "早安",
    "晚安",
    "哈哈",
    "笑死",
    "吃饭",
    "睡觉",
    "生日",
    "天气",
    "旅游",
    "日常",
    "相亲",
    "彩礼",
    "怀了",
    "宝宝",
    "主持人",
    "女孩子",
    "自拍",
    "抽奖",
    "转发抽",
    "giveaway",
]

CASHTAG_RE = re.compile(r"[$＄][A-Za-z][A-Za-z0-9_]{1,15}")
ADDRESS_RE = re.compile(r"\b0x[a-fA-F0-9]{30,}\b|solana:[A-Za-z0-9]{24,}")
URL_RE = re.compile(r"https?://\S+")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
    tmp_path.replace(path)


def compact_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def score_tweet(tweet: dict[str, Any]) -> dict[str, Any]:
    text = compact_text(tweet.get("text"))
    quoted_text = compact_text(tweet.get("quoted_text"))
    combined = f"{text} {quoted_text}".strip()
    lower = combined.lower()

    score = 0
    categories: set[str] = set()
    reasons: list[str] = []

    for category, weight, keywords in SIGNAL_RULES:
        hits = [keyword for keyword in keywords if keyword.lower() in lower]
        if hits:
            score += weight + min(len(hits) - 1, 3)
            categories.add(category)
            reasons.append(f"{category}:{','.join(hits[:5])}")

    cashtags = CASHTAG_RE.findall(combined)
    addresses = ADDRESS_RE.findall(combined)
    if cashtags:
        score += 3
        categories.add("asset_reference")
        reasons.append(f"cashtag:{','.join(cashtags[:5])}")
    if addresses:
        score += 4
        categories.add("asset_reference")
        reasons.append("contract_address")

    text_length = len(combined)
    if text_length >= 220:
        score += 2
        reasons.append("longform")
    elif text_length <= 24:
        score -= 2
        reasons.append("very_short")

    views = int(tweet.get("views") or 0)
    likes = int(tweet.get("favorite_count") or 0)
    replies = int(tweet.get("reply_count") or 0)
    retweets = int(tweet.get("retweet_count") or 0)
    engagement = likes + replies * 2 + retweets * 3
    if views >= 50000 or engagement >= 100:
        score += 2
        reasons.append("high_engagement")
    elif views >= 10000 or engagement >= 30:
        score += 1
        reasons.append("medium_engagement")

    noise_hits = [keyword for keyword in NOISE_KEYWORDS if keyword.lower() in lower]
    if noise_hits and score < 8:
        score -= 4
        categories.add("noise_candidate")
        reasons.append(f"noise:{','.join(noise_hits[:3])}")

    urls = URL_RE.findall(combined)
    if urls and score < 6:
        categories.add("link_only")
        reasons.append("link_retained")

    return {
        "score": score,
        "categories": sorted(categories),
        "reasons": reasons,
        "urls": sorted(set(urls)),
    }


def knowledge_record(tweet: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    text = compact_text(tweet.get("text"))
    quoted_text = compact_text(tweet.get("quoted_text"))
    return {
        "source": "twitter",
        "username": tweet.get("username"),
        "tweet_id": tweet.get("tweet_id"),
        "url": tweet.get("url"),
        "created_at": tweet.get("created_at"),
        "categories": meta["categories"],
        "score": meta["score"],
        "text": text,
        "quoted_text": quoted_text,
        "metrics": {
            "views": tweet.get("views"),
            "likes": tweet.get("favorite_count"),
            "retweets": tweet.get("retweet_count"),
            "replies": tweet.get("reply_count"),
            "quotes": tweet.get("quote_count"),
        },
        "filter_reasons": meta["reasons"],
    }


def link_record(tweet: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "twitter",
        "username": tweet.get("username"),
        "tweet_id": tweet.get("tweet_id"),
        "url": tweet.get("url"),
        "created_at": tweet.get("created_at"),
        "linked_urls": meta["urls"],
        "text_preview": compact_text(tweet.get("text"))[:240],
        "score": meta["score"],
        "filter_reasons": meta["reasons"],
    }


def summarize(username: str, total: int, knowledge: int, links: int, excluded: int) -> str:
    return (
        f"# {username} Twitter Knowledge Summary\n\n"
        f"- Total normalized tweets: {total}\n"
        f"- Knowledge records: {knowledge}\n"
        f"- Link-only records: {links}\n"
        f"- Excluded/noise records: {excluded}\n"
    )


def build_for_user(user_dir: Path, threshold: int) -> None:
    input_path = user_dir / "sources" / "twitter" / "normalized" / "tweets.jsonl"
    if not input_path.exists():
        print(f"skip {user_dir.name}: missing {input_path}")
        return

    tweets = read_jsonl(input_path)
    knowledge_rows: list[dict[str, Any]] = []
    link_rows: list[dict[str, Any]] = []
    excluded_rows: list[dict[str, Any]] = []

    for tweet in tweets:
        meta = score_tweet(tweet)
        if meta["score"] >= threshold:
            knowledge_rows.append(knowledge_record(tweet, meta))
        elif meta["urls"]:
            link_rows.append(link_record(tweet, meta))
        else:
            excluded_rows.append(
                {
                    "tweet_id": tweet.get("tweet_id"),
                    "url": tweet.get("url"),
                    "created_at": tweet.get("created_at"),
                    "score": meta["score"],
                    "filter_reasons": meta["reasons"],
                    "text_preview": compact_text(tweet.get("text"))[:160],
                }
            )

    knowledge_dir = user_dir / "knowledge"
    write_jsonl(knowledge_dir / "twitter_knowledge.jsonl", knowledge_rows)
    write_jsonl(knowledge_dir / "twitter_links.jsonl", link_rows)
    write_jsonl(knowledge_dir / "twitter_excluded.jsonl", excluded_rows)
    summary_path = knowledge_dir / "twitter_summary.md"
    summary_path.write_text(
        summarize(
            user_dir.name,
            len(tweets),
            len(knowledge_rows),
            len(link_rows),
            len(excluded_rows),
        ),
        encoding="utf-8",
    )
    print(
        f"{user_dir.name}: {len(knowledge_rows)} knowledge, "
        f"{len(link_rows)} link-only, {len(excluded_rows)} excluded"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build filtered Twitter knowledge files from archived KOL timelines."
    )
    parser.add_argument("handles", nargs="*", help="Handle folders under data/users")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR)
    parser.add_argument("--threshold", type=int, default=6)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.handles:
        user_dirs = [args.users_dir / handle.lstrip("@") for handle in args.handles]
    else:
        if not args.users_dir.exists():
            print(f"No users directory found: {args.users_dir}")
            return 0
        user_dirs = sorted(path for path in args.users_dir.iterdir() if path.is_dir())
    for user_dir in user_dirs:
        build_for_user(user_dir, args.threshold)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
