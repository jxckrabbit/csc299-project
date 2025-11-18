import os
import json
from src import storage


def test_save_and_load(tmp_path, monkeypatch):
    f = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(f))
    data = {"users": [], "tasks": []}
    storage.save_data(data)
    assert f.exists()
    loaded = storage.load_data()
    assert loaded == data
