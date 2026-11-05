
"""
Модуль test_logic.py.
Содержит Unit-тесты бизнес-логики менеджера задач.
"""

import db
import logic
import pytest


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Создаёт отдельную базу данных для каждого теста."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()


def test_validate_title():
    """Проверяет обработку корректного названия."""
    assert logic.validate_title("  Подготовить отчёт  ") == (
        "Подготовить отчёт"
    )


@pytest.mark.parametrize("title", ["", "   "])
def test_validate_empty_title(title):
    """Проверяет отклонение пустого названия."""
    with pytest.raises(ValueError):
        logic.validate_title(title)


def test_validate_priority():
    """Проверяет нормализацию приоритета."""
    assert logic.validate_priority("ВЫСОКИЙ") == "Высокий"
    assert logic.validate_priority(" средний ") == "Средний"
    assert logic.validate_priority("низкий") == "Низкий"


def test_invalid_priority():
    """Проверяет отклонение неправильного приоритета."""
    with pytest.raises(ValueError):
        logic.validate_priority("Срочный")


def test_validate_status():
    """Проверяет нормализацию статуса."""
    assert logic.validate_status("новая") == "Новая"
    assert logic.validate_status("В РАБОТЕ") == "В работе"
    assert logic.validate_status("выполнено") == "Выполнено"


def test_invalid_status():
    """Проверяет отклонение неправильного статуса."""
    with pytest.raises(ValueError):
        logic.validate_status("Отложена")


def test_sort_tasks_by_priority():
    """Проверяет сортировку от высокого приоритета к низкому."""
    tasks = [
        {"id": 1, "priority": "Низкий"},
        {"id": 2, "priority": "Высокий"},
        {"id": 3, "priority": "Средний"}
    ]

    result = logic.sort_tasks_by_priority(tasks)

    assert [task["id"] for task in result] == [2, 3, 1]
    assert [task["id"] for task in tasks] == [1, 2, 3]


def test_sort_same_priority():
    """Проверяет порядок задач с одинаковым приоритетом."""
    tasks = [
        {"id": 1, "priority": "Высокий"},
        {"id": 2, "priority": "Высокий"}
    ]

    result = logic.sort_tasks_by_priority(tasks)

    assert [task["id"] for task in result] == [1, 2]


def test_create_and_get_tasks(isolated_db):
    """Проверяет создание и получение отсортированных задач."""
    logic.create_task("  Обычная задача  ", "", "низкий")
    logic.create_task("Срочная задача", "Описание", "ВЫСОКИЙ")

    tasks = logic.get_tasks()

    assert len(tasks) == 2
    assert tasks[0]["priority"] == "Высокий"
    assert tasks[1]["priority"] == "Низкий"
    assert tasks[0]["status"] == "Новая"
    assert tasks[1]["title"] == "Обычная задача"


def test_change_task_status(isolated_db):
    """Проверяет изменение статуса задачи."""
    task_id = logic.create_task("Задача", "", "Средний")

    result = logic.change_task_status(task_id, "выполнено")

    assert result is True
    assert logic.get_tasks()[0]["status"] == "Выполнено"


def test_remove_task(isolated_db):
    """Проверяет удаление задачи."""
    task_id = logic.create_task("Задача", "", "Низкий")

    assert logic.remove_task(task_id) is True
    assert logic.get_tasks() == []


def test_invalid_task_id():
    """Проверяет отклонение неправильного ID."""
    with pytest.raises(ValueError):
        logic.remove_task(0)
