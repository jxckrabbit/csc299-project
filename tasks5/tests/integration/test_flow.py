import subprocess
import os
import sys


def run_cmd(args, env=None):
    cmd = [sys.executable, "-m", "src.cli"] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return res


def test_end_to_end(tmp_path, monkeypatch):
    f = tmp_path / "tasks.json"
    env = os.environ.copy()
    env["TASKS_FILE"] = str(f)

    # create user
    r = run_cmd(["create-user", "Bob"], env=env)
    assert r.returncode == 0
    user_id = r.stdout.strip().split()[-1]

    # add task
    r = run_cmd(["add-task", user_id, "--title", "Pay rent", "--due", "2025-12-01", "--category", "finance"], env=env)
    assert r.returncode == 0
    task_id = r.stdout.strip().split()[-1]

    # list tasks
    r = run_cmd(["list-tasks", user_id], env=env)
    assert "Pay rent" in r.stdout

    # remove task
    r = run_cmd(["remove-task", user_id, task_id], env=env)
    assert r.returncode == 0

    # list tasks should not contain the task
    r = run_cmd(["list-tasks", user_id], env=env)
    assert "Pay rent" not in r.stdout
