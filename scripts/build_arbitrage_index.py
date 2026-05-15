#!/usr/bin/env python3
"""
Build focused indexes for arbitrage strategy records.
"""

from __future__ import annotations

import json
import sys
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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
    tmp_path.replace(path)


def compact_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "username": row.get("username"),
        "tweet_id": row.get("tweet_id"),
        "url": row.get("url"),
        "created_at": row.get("created_at"),
        "score": row.get("score"),
        "categories": row.get("categories") or [],
        "text": row.get("text"),
        "quoted_text": row.get("quoted_text"),
        "media_urls": row.get("media_urls") or [],
        "metrics": row.get("metrics") or {},
        "filter_reasons": row.get("filter_reasons") or [],
    }


def build(users_dir: Path, index_dir: Path) -> None:
    arbitrage: list[dict[str, Any]] = []
    visual: list[dict[str, Any]] = []
    for user_dir in sorted(path for path in users_dir.iterdir() if path.is_dir()):
        rows = read_jsonl(user_dir / "knowledge" / "twitter_knowledge.jsonl")
        for row in rows:
            categories = set(row.get("categories") or [])
            if "arbitrage_strategy" not in categories:
                continue
            record = compact_record(row)
            arbitrage.append(record)
            if record["media_urls"]:
                visual.append(record)

    arbitrage.sort(key=lambda row: (row.get("score") or 0, row.get("created_at") or ""), reverse=True)
    visual.sort(key=lambda row: (row.get("score") or 0, row.get("created_at") or ""), reverse=True)

    write_jsonl(index_dir / "arbitrage_strategies.jsonl", arbitrage)
    write_jsonl(index_dir / "arbitrage_visual_strategies.jsonl", visual)
    print(f"indexed {len(arbitrage)} arbitrage records, {len(visual)} with media")


def main(argv: list[str]) -> int:
    users_dir = Path(argv[0]) if argv else DEFAULT_USERS_DIR
    index_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_INDEX_DIR
    if not users_dir.exists():
        print(f"No users directory found: {users_dir}")
        return 0
    build(users_dir, index_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
