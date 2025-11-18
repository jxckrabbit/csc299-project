import json
import os
import tempfile
from typing import Dict, Any


def _tasks_file() -> str:
    return os.environ.get("TASKS_FILE", os.path.join("data", "tasks.json"))


def load_data() -> Dict[str, Any]:
    path = _tasks_file()
    if not os.path.exists(path):
        return {"users": [], "tasks": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(obj: Dict[str, Any]) -> None:
    path = _tasks_file()
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    # atomic write: write to temp file then replace
    fd, tmp = tempfile.mkstemp(dir=dirpath or None)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass
