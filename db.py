"""
Модуль db.py.
Содержит функции для работы с базой данных задач SQLite.
"""

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "project.db"


def get_connection() -> sqlite3.Connection:
    """
    @brief Создаёт подключение к базе данных.

    @return Объект подключения SQLite.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """
    @brief Создаёт таблицу задач, если она не существует.

    @return None
    """
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK (
                    length(trim(title)) > 0
                ),
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL CHECK (
                    priority IN ('Низкий', 'Средний', 'Высокий')
                ),
                status TEXT NOT NULL DEFAULT 'новая' CHECK (
                    status IN ('Новая', 'В работе', 'Выполнено')
                )
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def add_item(
    title: str,
    description: str,
    priority: str
) -> int:
    """
    @brief Добавляет новую задачу в базу данных.

    @param title Название задачи.
    @param description Описание задачи.
    @param priority Приоритет задачи.
    @return Идентификатор созданной задачи.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, priority)
            VALUES (?, ?, ?)
            """,
            (title, description, priority)
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_all_items() -> list[dict]:
    """
    @brief Получает все задачи из базы данных.

    @return Список словарей с данными задач.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM tasks ORDER BY id"
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def update_status(item_id: int, status: str) -> bool:
    """
    @brief Изменяет статус указанной задачи.

    @param item_id Идентификатор задачи.
    @param status Новый статус.
    @return True, если задача найдена и обновлена.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, item_id)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_item(item_id: int) -> bool:
    """
    @brief Удаляет задачу по идентификатору.

    @param item_id Идентификатор задачи.
    @return True, если задача была удалена.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (item_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_statistics() -> dict:
    """
    @brief Подсчитывает статистику задач.

    @return Количество всех, выполненных
            и невыполненных задач.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(CASE WHEN status = 'Выполнено'
                      THEN 1 END) AS completed,
                COUNT(CASE WHEN status != 'Выполнено'
                      THEN 1 END) AS not_completed
            FROM tasks
            """
        )
        return dict(cursor.fetchone())
    finally:
        connection.close()


if __name__ == "__main__":
    init_db()
    print("База данных и таблица tasks готовы.")
