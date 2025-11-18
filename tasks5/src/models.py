from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Optional
import uuid


def new_id() -> str:
    return uuid.uuid4().hex


@dataclass
class User:
    id: str
    display_name: str

    @staticmethod
    def create(display_name: str) -> "User":
        name = display_name.strip()
        if not name:
            raise ValueError("display_name must be non-empty")
        return User(id=new_id(), display_name=name)


@dataclass
class Task:
    id: str
    user_id: str
    title: str
    due_date: str
    category: Optional[str]
    created_at: str

    @staticmethod
    def create(user_id: str, title: str, due_date: str, category: Optional[str] = None) -> "Task":
        t = title.strip()
        if not t:
            raise ValueError("title must be non-empty")
        # validate due_date is YYYY-MM-DD
        try:
            _ = date.fromisoformat(due_date)
        except Exception:
            raise ValueError("due_date must be ISO YYYY-MM-DD")
        if category is not None and len(category) > 50:
            raise ValueError("category too long")
        return Task(id=new_id(), user_id=user_id, title=t, due_date=due_date, category=category, created_at=datetime.utcnow().isoformat() + "Z")


def to_dict(obj):
    return asdict(obj)
