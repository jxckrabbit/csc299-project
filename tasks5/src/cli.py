import argparse
import sys
from typing import Optional

from . import models
from . import storage


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def cmd_list_users(args):
    data = storage.load_data()
    users = sorted(data.get("users", []), key=lambda u: u.get("display_name", ""))
    for u in users:
        print(f"{u['id']}\t{u['display_name']}")
    return 0


def cmd_create_user(args):
    name = args.display_name
    try:
        user = models.User.create(name)
    except ValueError as e:
        eprint(f"ERROR 2 {e}")
        return 2
    data = storage.load_data()
    data.setdefault("users", []).append({"id": user.id, "display_name": user.display_name})
    storage.save_data(data)
    print(f"CREATED {user.id}")
    return 0


def _find_user(data, user_id):
    for u in data.get("users", []):
        if u["id"] == user_id:
            return u
    return None


def cmd_list_tasks(args):
    user_id = args.user_id
    data = storage.load_data()
    user = _find_user(data, user_id)
    if not user:
        eprint("ERROR 3 user-not-found")
        return 3
    tasks = [t for t in data.get("tasks", []) if t.get("user_id") == user_id]
    tasks_sorted = sorted(tasks, key=lambda t: t.get("due_date", ""))
    for t in tasks_sorted:
        print(f"{t['id']}\t{t['due_date']}\t{t.get('category','')}\t{t['title']}")
    return 0


def cmd_add_task(args):
    user_id = args.user_id
    title = args.title
    due = args.due
    category = args.category
    data = storage.load_data()
    user = _find_user(data, user_id)
    if not user:
        eprint("ERROR 3 user-not-found")
        return 3
    try:
        task = models.Task.create(user_id=user_id, title=title, due_date=due, category=category)
    except ValueError as e:
        eprint(f"ERROR 2 {e}")
        return 2
    data.setdefault("tasks", []).append({
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "due_date": task.due_date,
        "category": task.category,
        "created_at": task.created_at,
    })
    storage.save_data(data)
    print(f"TASK-ADDED {task.id}")
    return 0


def cmd_remove_task(args):
    user_id = args.user_id
    task_id = args.task_id
    data = storage.load_data()
    user = _find_user(data, user_id)
    if not user:
        eprint("ERROR 3 user-not-found")
        return 3
    tasks = data.get("tasks", [])
    for i, t in enumerate(tasks):
        if t.get("id") == task_id and t.get("user_id") == user_id:
            del tasks[i]
            storage.save_data(data)
            print(f"TASK-REMOVED {task_id}")
            return 0
    eprint("ERROR 4 task-not-found")
    return 4


def main(argv=None):
    parser = argparse.ArgumentParser(prog="taskmgr")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-users")

    p = sub.add_parser("create-user")
    p.add_argument("display_name")

    p = sub.add_parser("list-tasks")
    p.add_argument("user_id")

    p = sub.add_parser("add-task")
    p.add_argument("user_id")
    p.add_argument("--title", required=True)
    p.add_argument("--due", required=True)
    p.add_argument("--category", default=None)

    p = sub.add_parser("remove-task")
    p.add_argument("user_id")
    p.add_argument("task_id")

    args = parser.parse_args(argv)
    if args.cmd == "list-users":
        return cmd_list_users(args)
    if args.cmd == "create-user":
        return cmd_create_user(args)
    if args.cmd == "list-tasks":
        return cmd_list_tasks(args)
    if args.cmd == "add-task":
        return cmd_add_task(args)
    if args.cmd == "remove-task":
        return cmd_remove_task(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
