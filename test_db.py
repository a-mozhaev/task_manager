
"""
Модуль test_db.py.
Содержит Unit-тесты базы данных SQLite.
"""

import sqlite3

import db
import pytest


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Создаёт временную базу данных для теста."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()


def test_init_db(isolated_db):
    """Проверяет создание таблицы tasks."""
    db.init_db()

    connection = db.get_connection()
    try:
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(tasks)")
        }
    finally:
        connection.close()

    assert columns == {
        "id", "title", "description", "priority", "status"
    }


def test_add_and_get_items(isolated_db):
    """Проверяет добавление и получение задачи."""
    task_id = db.add_item(
        "Подготовить отчёт", "Описание", "Высокий"
    )

    tasks = db.get_all_items()

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Подготовить отчёт"
    assert tasks[0]["priority"] == "Высокий"
    assert tasks[0]["status"] == "Новая"


def test_update_status(isolated_db):
    """Проверяет изменение статуса задачи."""
    task_id = db.add_item("Задача", "", "Средний")

    assert db.update_status(task_id, "Выполнено") is True
    assert db.get_all_items()[0]["status"] == "Выполнено"


def test_update_missing_task(isolated_db):
    """Проверяет изменение несуществующей задачи."""
    assert db.update_status(999, "Выполнено") is False


def test_delete_item(isolated_db):
    """Проверяет удаление задачи."""
    task_id = db.add_item("Задача", "", "Низкий")

    assert db.delete_item(task_id) is True
    assert db.get_all_items() == []
    assert db.delete_item(task_id) is False


def test_get_statistics(isolated_db):
    """Проверяет подсчёт статистики задач."""
    id1 = db.add_item("Задача 1", "", "Высокий")
    id2 = db.add_item("Задача 2", "", "Средний")
    db.add_item("Задача 3", "", "Низкий")

    db.update_status(id1, "Выполнено")
    db.update_status(id2, "В работе")

    statistics = db.get_statistics()

    assert statistics == {
        "total": 3,
        "completed": 1,
        "not_completed": 2
    }


def test_empty_title(isolated_db):
    """Проверяет ограничение на пустое название."""
    with pytest.raises(sqlite3.IntegrityError):
        db.add_item("   ", "", "Высокий")


def test_invalid_priority(isolated_db):
    """Проверяет ограничение допустимых приоритетов."""
    with pytest.raises(sqlite3.IntegrityError):
        db.add_item("Задача", "", "Срочный")


def test_invalid_status(isolated_db):
    """Проверяет ограничение допустимых статусов."""
    task_id = db.add_item("Задача", "", "Средний")

    with pytest.raises(sqlite3.IntegrityError):
        db.update_status(task_id, "Отложена")
