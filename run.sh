#!/bin/bash

# Останавливать скрипт при ошибке
set -e

# Переход в каталог проекта
cd "$(dirname "$0")"

# Активация виртуального окружения
source venv/bin/activate

# Запуск программы
python main.py
