import subprocess
import os
import sys


def run_cmd(args, env=None):
    cmd = [sys.executable, "-m", "src.cli"] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return res


def test_create_user_and_list(tmp_path, monkeypatch):
    f = tmp_path / "tasks.json"
    env = os.environ.copy()
    env["TASKS_FILE"] = str(f)
    res = run_cmd(["create-user", "Alice"], env=env)
    assert res.returncode == 0
    assert res.stdout.strip().startswith("CREATED")
    # list users
    res2 = run_cmd(["list-users"], env=env)
    assert "Alice" in res2.stdout
