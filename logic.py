
"""
Модуль logic.py.
Содержит бизнес-логику менеджера задач.
"""

import db


PRIORITY_ORDER = {
    "Высокий": 0,
    "Средний": 1,
    "Низкий": 2
}

VALID_STATUSES = (
    "Новая",
    "В работе",
    "Выполнено"
)


def validate_title(title: str) -> str:
    """
    @brief Проверяет название задачи.

    @param title Название задачи.
    @return Название без лишних пробелов.
    @throws ValueError Если название пустое.
    """
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Название задачи не может быть пустым!")

    return title.strip()


def validate_priority(priority: str) -> str:
    """
    @brief Проверяет приоритет задачи.

    @param priority Приоритет задачи.
    @return Корректный приоритет.
    @throws ValueError Если приоритет недопустим.
    """
    if not isinstance(priority, str):
        raise ValueError("Некорректный приоритет!")

    priority = priority.strip().capitalize()

    if priority not in PRIORITY_ORDER:
        raise ValueError("Приоритет: Низкий, Средний или Высокий!")

    return priority


def validate_status(status: str) -> str:
    """
    @brief Проверяет статус задачи.

    @param status Статус задачи.
    @return Корректный статус.
    @throws ValueError Если статус недопустим.
    """
    if not isinstance(status, str):
        raise ValueError("Некорректный статус!")

    status = status.strip().capitalize()

    if status not in VALID_STATUSES:
        raise ValueError("Статус: Новая, В работе или Выполнено!")

    return status


def validate_task_id(task_id: int) -> int:
    """
    @brief Проверяет идентификатор задачи.

    @param task_id Идентификатор задачи.
    @return Корректный идентификатор.
    @throws ValueError Если идентификатор недопустим.
    """
    if type(task_id) is not int or task_id <= 0:
        raise ValueError("ID задачи должен быть положительным числом!")

    return task_id



def sort_tasks_by_priority(tasks: list[dict]) -> list[dict]:
    """
    @brief Сортирует задачи по приоритету и идентификатору.

    @param tasks Список задач.
    @return Список задач, отсортированный по приоритету
            и возрастанию идентификатора.
    """
    return sorted(
        tasks,
        key=lambda task: (
            PRIORITY_ORDER[task["priority"]],
            task["id"]
        )
    )


def create_task(
    title: str,
    description: str,
    priority: str
) -> int:
    """
    @brief Создаёт новую задачу.

    @param title Название задачи.
    @param description Описание задачи.
    @param priority Приоритет задачи.
    @return Идентификатор созданной задачи.
    @throws ValueError При некорректных данных.
    """
    title = validate_title(title)
    priority = validate_priority(priority)

    if not isinstance(description, str):
        raise ValueError("Описание задачи должно быть текстом!")

    return db.add_item(title, description.strip(), priority)


def get_tasks() -> list[dict]:
    """
    @brief Получает задачи, отсортированные по приоритету.

    @return Список задач.
    """
    tasks = db.get_all_items()
    return sort_tasks_by_priority(tasks)


def change_task_status(task_id: int, status: str) -> bool:
    """
    @brief Изменяет статус задачи.

    @param task_id Идентификатор задачи.
    @param status Новый статус.
    @return True, если задача обновлена.
    """
    task_id = validate_task_id(task_id)
    status = validate_status(status)

    return db.update_status(task_id, status)


def remove_task(task_id: int) -> bool:
    """
    @brief Удаляет задачу.

    @param task_id Идентификатор задачи.
    @return True, если задача удалена.
    """
    task_id = validate_task_id(task_id)
    return db.delete_item(task_id)


def get_statistics() -> dict:
    """
    @brief Получает статистику задач.

    @return Словарь со статистикой.
    """
    return db.get_statistics()
