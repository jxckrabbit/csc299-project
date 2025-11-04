import os
import sys
import tempfile
import json
import pytest
from argparse import Namespace

# Ensure the package directory (src) is on sys.path so `from tasks3 import ...` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import tasks3 as todo

# Helper to create a temp tasks file and clean up
def temp_tasks_file(data=None):
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    if data is not None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return path

def test_add_and_load_tasks():
    path = temp_tasks_file([])
    args = Namespace(title="Test Task", tags="work,urgent", category="work", file=path)
    todo.cmd_add(args)
    tasks = todo.load_tasks(path)
    assert len(tasks) == 1
    t = tasks[0]
    assert t.title == "Test Task"
    assert set(t.tags) == {"work", "urgent"}
    assert t.category == "work"
    os.remove(path)

def test_save_and_load_tasks():
    path = temp_tasks_file([])
    tasks = [todo.Task(id=1, title="A", created="2023-01-01T00:00:00Z", tags=["x"], category="c")]
    todo.save_tasks(path, tasks)
    loaded = todo.load_tasks(path)
    assert loaded[0].title == "A"
    os.remove(path)

def test_next_id():
    tasks = [todo.Task(id=1, title="A", created="", tags=[]), todo.Task(id=3, title="B", created="", tags=[])]
    assert todo.next_id(tasks) == 4
    assert todo.next_id([]) == 1

def test_cmd_list_prints_tasks(capsys):
    path = temp_tasks_file([
        {"id": 1, "title": "T1", "created": "", "tags": ["a"], "category": "cat", "done": False},
        {"id": 2, "title": "T2", "created": "", "tags": ["b"], "category": "cat", "done": True},
    ])
    args = Namespace(file=path, all=True, tags=None, category=None)
    todo.cmd_list(args)
    out = capsys.readouterr().out
    assert "T1" in out and "T2" in out
    args = Namespace(file=path, all=False, tags=None, category=None)
    todo.cmd_list(args)
    out = capsys.readouterr().out
    assert "T1" in out and "T2" not in out
    os.remove(path)

def test_cmd_search(capsys):
    path = temp_tasks_file([
        {"id": 1, "title": "Buy milk", "created": "", "tags": ["shopping"], "category": "home", "done": False},
        {"id": 2, "title": "Read book", "created": "", "tags": ["leisure"], "category": "home", "done": False},
    ])
    args = Namespace(file=path, query="milk", category=None)
    todo.cmd_search(args)
    out = capsys.readouterr().out
    assert "Buy milk" in out
    args = Namespace(file=path, query="leisure", category=None)
    todo.cmd_search(args)
    out = capsys.readouterr().out
    assert "Read book" in out
    args = Namespace(file=path, query="milk", category="home")
    todo.cmd_search(args)
    out = capsys.readouterr().out
    assert "Buy milk" in out
    os.remove(path)

def test_cmd_recommend(capsys):
    path = temp_tasks_file([
        {"id": 1, "title": "A", "created": "", "tags": ["x"], "category": "c", "done": False},
        {"id": 2, "title": "B", "created": "", "tags": ["y"], "category": "c", "done": False},
    ])
    args = Namespace(file=path, count=1, all=False, tags=None, category=None)
    todo.cmd_recommend(args)
    out = capsys.readouterr().out
    assert "Recommended 1 task" in out
    args = Namespace(file=path, count=2, all=True, tags="x", category="c")
    todo.cmd_recommend(args)
    out = capsys.readouterr().out
    assert "A" in out
    os.remove(path)

def test_format_task():
    t = todo.Task(id=1, title="T", created="now", tags=["a", "b"], category="cat", done=True)
    s = todo.format_task(t)
    assert "[x]" in s and "a, b" in s and "cat" in s

def test_main_prints_help(capsys):
    # No args should print help
    ret = todo.main([])
    out = capsys.readouterr().out
    assert "usage" in out.lower()
    assert ret == 1
