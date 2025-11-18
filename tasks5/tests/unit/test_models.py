from src import models
import pytest


def test_user_create_valid():
    u = models.User.create("Alice")
    assert u.display_name == "Alice"
    assert u.id


def test_user_create_invalid():
    with pytest.raises(ValueError):
        models.User.create("")


def test_task_create_valid():
    t = models.Task.create(user_id="u1", title="Buy milk", due_date="2025-11-19", category="errands")
    assert t.title == "Buy milk"
    assert t.user_id == "u1"


def test_task_create_invalid_title():
    with pytest.raises(ValueError):
        models.Task.create(user_id="u1", title="  ", due_date="2025-11-19")


def test_task_create_invalid_date():
    with pytest.raises(ValueError):
        models.Task.create(user_id="u1", title="x", due_date="not-a-date")
