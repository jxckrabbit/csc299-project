#!/usr/bin/env python3
"""Simple task manager CLI.

Usage:
  python todo.py add "Task title" --tags tag1,tag2
  python todo.py list [--all] [--tags tag]
  python todo.py search "query"

Tasks stored in `tasks.json` next to this script by default.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
import random
from typing import List, Optional


DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


@dataclass
class Task:
    id: int
    title: str
    created: str
    tags: List[str]
    category: str = "general"
    done: bool = False


def load_tasks(path: str) -> List[Task]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    tasks = []
    for item in data:
        tasks.append(Task(**item))
    return tasks


def save_tasks(path: str, tasks: List[Task]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, indent=2, ensure_ascii=False)


def next_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1


def cmd_add(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.file)
    tid = next_id(tasks)
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    # choose provided category or fall back to Task default
    category = args.category if getattr(args, "category", None) else "general"
    t = Task(id=tid, title=args.title, created=datetime.utcnow().isoformat() + "Z", tags=tags, category=category)
    tasks.append(t)
    save_tasks(args.file, tasks)
    print(f"Added task {t.id}: {t.title}")
    return 0


def format_task(t: Task) -> str:
    tags = f" [{', '.join(t.tags)}]" if t.tags else ""
    status = "x" if t.done else " "
    return f"{t.id:3d}. [{status}] {t.title}{tags} <{t.category}> (created: {t.created})"


def cmd_list(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.file)
    if not tasks:
        print("No tasks.")
        return 0
    filtered = tasks
    if not args.all:
        filtered = [t for t in tasks if not t.done]
    if args.tags:
        tags = [x.strip() for x in args.tags.split(",")]
        filtered = [t for t in filtered if any(tag in t.tags for tag in tags)]
    if getattr(args, "category", None):
        filtered = [t for t in filtered if t.category == args.category]
    for t in sorted(filtered, key=lambda x: x.id):
        print(format_task(t))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    tasks = load_tasks(args.file)
    q = args.query.lower()
    matches = [t for t in tasks if q in t.title.lower() or any(q in tag.lower() for tag in t.tags)]
    if not matches:
        print("No matches found.")
        return 0
    if getattr(args, "category", None):
        matches = [t for t in matches if t.category == args.category]
    for t in sorted(matches, key=lambda x: x.id):
        print(format_task(t))
    return 0


def cmd_recommend(args: argparse.Namespace) -> int:
    """Recommend a number of tasks to complete at random.

    Behavior:
    - By default only incomplete tasks are considered (unless --all is set).
    - Supports optional --category and --tags filters (comma-separated tags).
    - If fewer tasks are available than requested, all matching tasks are returned.
    """
    tasks = load_tasks(args.file)
    if not tasks:
        print("No tasks.")
        return 0
    candidates = tasks
    if not args.all:
        candidates = [t for t in tasks if not t.done]
    if args.tags:
        tags = [x.strip() for x in args.tags.split(",")]
        candidates = [t for t in candidates if any(tag in t.tags for tag in tags)]
    if getattr(args, "category", None):
        candidates = [t for t in candidates if t.category == args.category]

    if not candidates:
        print("No matching tasks to recommend.")
        return 0

    try:
        count = int(args.count)
    except (TypeError, ValueError):
        print("Invalid count; please provide an integer number of tasks to recommend.")
        return 1

    k = min(count, len(candidates))
    picks = random.sample(candidates, k)
    print(f"Recommended {k} task(s):")
    for t in sorted(picks, key=lambda x: x.id):
        print(format_task(t))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Simple JSON-backed todo CLI")
    p.add_argument("--file", "-f", default=DEFAULT_DATA_FILE, help="tasks JSON file")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("add", help="Add a new task")
    pa.add_argument("title", help="Task title")
    pa.add_argument("--tags", help="Comma-separated tags", default="")
    pa.add_argument("--category", help="Task category (e.g. household, schoolwork)", default="")
    pa.set_defaults(func=cmd_add)

    pl = sub.add_parser("list", help="List tasks")
    pl.add_argument("--all", action="store_true", help="Include completed tasks")
    pl.add_argument("--tags", help="Filter by comma-separated tags")
    pl.add_argument("--category", help="Filter by category (exact match)")
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("search", help="Search tasks by text or tag")
    ps.add_argument("query", help="Search query")
    ps.add_argument("--category", help="Filter search by category (exact match)")
    ps.set_defaults(func=cmd_search)

    pr = sub.add_parser("recommend", help="Recommend N random tasks to complete")
    pr.add_argument("count", help="Number of tasks to recommend")
    pr.add_argument("--all", action="store_true", help="Include completed tasks as candidates")
    pr.add_argument("--tags", help="Filter candidates by comma-separated tags")
    pr.add_argument("--category", help="Filter candidates by category (exact match)")
    pr.set_defaults(func=cmd_recommend)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    # ensure data dir exists
    d = os.path.dirname(args.file)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    return args.func(args)