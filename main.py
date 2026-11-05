
"""
Модуль main.py.
Содержит консольный интерфейс менеджера задач.
"""

import db
import logic


def read_task_id() -> int:
    """
    @brief Запрашивает идентификатор задачи.

    @return Введённый идентификатор.
    @throws ValueError Если введено не целое число.
    """
    value = input("Введите ID задачи: ").strip()

    try:
        return int(value)
    except ValueError:
        raise ValueError("ID задачи должен быть целым числом!") from None


def add_task() -> None:
    """
    @brief Запрашивает данные и создаёт новую задачу.

    @return None
    """
    print("\n--- Добавление задачи ---")

    title = input("Название задачи: ")
    description = input("Описание задачи: ")

    print("Приоритеты: Высокий, Средний, Низкий")
    priority = input("Приоритет задачи: ")

    try:
        task_id = logic.create_task(
            title, description, priority
        )
        print(f"Задача успешно создана! ID: {task_id}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def show_tasks() -> None:
    """
    @brief Выводит задачи в порядке убывания приоритета.

    @return None
    """
    print("\n--- Список задач ---")

    tasks = logic.get_tasks()

    if not tasks:
        print("Список задач пуст.")
        return

    for task in tasks:
        print(
            f"\nID: {task['id']} | "
            f"Название: {task['title']}"
        )
        print(f"Приоритет: {task['priority']}")
        print(f"Статус: {task['status']}")

        if task["description"]:
            print(f"Описание: {task['description']}")


def change_status() -> None:
    """
    @brief Изменяет статус выбранной задачи.

    @return None
    """
    print("\n--- Изменение статуса задачи ---")

    try:
        task_id = read_task_id()

        print("Статусы: Новая, В работе, Выполнено")
        status = input("Новый статус: ")

        if logic.change_task_status(task_id, status):
            print("Статус задачи успешно изменён!")
        else:
            print("Задача с указанным ID не найдена.")

    except ValueError as error:
        print(f"Ошибка: {error}")


def delete_task() -> None:
    """
    @brief Удаляет выбранную задачу.

    @return None
    """
    print("\n--- Удаление задачи ---")

    try:
        task_id = read_task_id()

        if logic.remove_task(task_id):
            print("Задача успешно удалена!")
        else:
            print("Задача с указанным ID не найдена.")

    except ValueError as error:
        print(f"Ошибка: {error}")


def show_statistics() -> None:
    """
    @brief Выводит статистику задач.

    @return None
    """
    print("\n--- Статистика задач ---")

    statistics = logic.get_statistics()

    print(f"Всего задач: {statistics['total']}")
    print(f"Выполнено: {statistics['completed']}")
    print(f"Не выполнено: {statistics['not_completed']}")


def main() -> None:
    """
    @brief Запускает главное меню менеджера задач.

    @return None
    """
    db.init_db()

    while True:
        print("\n========== МЕНЕДЖЕР ЗАДАЧ ==========")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Изменить статус задачи")
        print("4. Удалить задачу")
        print("5. Показать статистику")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            change_status()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            show_statistics()
        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Ошибка: выберите пункт от 0 до 5.")


if __name__ == "__main__":
    main()
