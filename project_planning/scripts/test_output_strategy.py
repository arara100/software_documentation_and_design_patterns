#!/usr/bin/env python3
"""
ЛР4: Демонстрація паттерну Strategy для виводу даних.

Цей скрипт показує, як паттерн Strategy дозволяє переключатися
між різними стратегіями виводу без змін у коді.

Користування:
    # Вивід в консоль (за замовчуванням)
    python3 scripts/test_output_strategy.py

    # Вивід в файл
    OUTPUT_STRATEGY=file python3 scripts/test_output_strategy.py

    # Вивід в Kafka
    OUTPUT_STRATEGY=kafka python3 scripts/test_output_strategy.py

    # Вивід в Redis (pub/sub)
    OUTPUT_STRATEGY=redis python3 scripts/test_output_strategy.py

    # Вивід в Redis (list/черга)
    REDIS_MODE=list OUTPUT_STRATEGY=redis python3 scripts/test_output_strategy.py

    # Вивід в Firebase
    FIREBASE_DATABASE_URL=https://<project>.firebaseio.com \\
    FIREBASE_CREDENTIALS_PATH=firebase-credentials.json \\
    OUTPUT_STRATEGY=firebase python3 scripts/test_output_strategy.py
"""

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from infrastructure.config import Config
from infrastructure.di_container import DIContainer
from infrastructure.database import init_db, create_all_tables


def main():
    init_db(Config.DATABASE_URL)
    create_all_tables()

    print("\n" + "=" * 70)
    print("ЛР4: Strategy Pattern для виводу даних")
    print("=" * 70)
    print(f"✓ Активна стратегія: {Config.OUTPUT_STRATEGY.upper()}\n")

    container = DIContainer()
    plan_service = container.get_plan_service()
    output_strategy = container.get_output_strategy()

    output_strategy.output("🚀 Запуск тестування OutputStrategy паттерну")
    output_strategy.output(f"📝 CSV файл: {Config.CSV_FILE_PATH}")

    try:
        print("\n▶ Виконання імпорту CSV через PlanService...")
        print("  (Вивід буде оброблено через OutputStrategy)\n")

        result = plan_service.import_from_csv(Config.CSV_FILE_PATH)

        print("\n✅ Імпорт завершено успішно!")
        print(f"  Проектів: {result['projects']}")
        print(f"  Задач: {result['tasks']}")
        print(f"  Ресурсів: {result['resources']}")
        print(f"  Призначень: {result['assignments']}")

    except FileNotFoundError:
        print(f"❌ Помилка: CSV файл не знайдено: {Config.CSV_FILE_PATH}")
        sys.exit(1)
    except Exception as exc:
        print(f"❌ Помилка під час імпорту: {exc}")
        sys.exit(1)

    sample_tasks = [
        "Реалізувати REST API",
        "Написати модульні тести",
        "Налаштувати DevOps",
        "Документувати код",
    ]
    output_strategy.output_list(sample_tasks)

    print("\n" + "=" * 70)
    print("✓ Тестування паттерну Strategy завершено")
    print("=" * 70)
    print(f"\n📌 Для переключення стратегії встановіть змінну середовища:")
    print("   export OUTPUT_STRATEGY=console|kafka|file|redis|firebase")
    print(f"\n📌 Поточна стратегія: {Config.OUTPUT_STRATEGY.upper()}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()


import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from infrastructure.config import Config
from infrastructure.di_container import DIContainer
from infrastructure.database import init_db, create_all_tables


def main():
    """
    Демонстрація паттерну Strategy.
    """
    # Ініціалізація БД
    init_db(Config.DATABASE_URL)
    create_all_tables()
    
    print("\n" + "=" * 70)
    print("ЛР4: Strategy Pattern для виводу даних")
    print("=" * 70)
    print(f"✓ Активна стратегія: {Config.OUTPUT_STRATEGY.upper()}\n")

    # Ініціалізація контейнера залежностей з OutputStrategy
    container = DIContainer()
    plan_service = container.get_plan_service()
    output_strategy = container.get_output_strategy()

    # ─────────────────────────────────────────────────────────────────
    # 1. Демонстрація виводу одного повідомлення
    # ─────────────────────────────────────────────────────────────────
    output_strategy.output("🚀 Запуск тестування OutputStrategy паттерну")
    output_strategy.output(f"📝 CSV файл: {Config.CSV_FILE_PATH}")

    # ─────────────────────────────────────────────────────────────────
    # 2. Виконання імпорту CSV з виводом через OutputStrategy
    # ─────────────────────────────────────────────────────────────────
    try:
        print("\n▶ Виконання імпорту CSV через PlanService...")
        print("  (Вивід буде оброблено через OutputStrategy)\n")
        
        result = plan_service.import_from_csv(Config.CSV_FILE_PATH)
        
        print("\n✅ Імпорт завершено успішно!")
        print(f"  Проектів: {result['projects']}")
        print(f"  Задач: {result['tasks']}")
        print(f"  Ресурсів: {result['resources']}")
        print(f"  Призначень: {result['assignments']}")

    except FileNotFoundError:
        print(f"❌ Помилка: CSV файл не знайдено: {Config.CSV_FILE_PATH}")
        sys.exit(1)
    except Exception as exc:
        print(f"❌ Помилка під час імпорту: {exc}")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────
    # 3. Демонстрація виводу списку
    # ─────────────────────────────────────────────────────────────────
    sample_tasks = [
        "Реалізувати REST API",
        "Написати модульні тести",
        "Налаштувати DevOps",
        "Документувати код",
    ]
    output_strategy.output_list(sample_tasks)

    # ─────────────────────────────────────────────────────────────────
    # 4. Завершення
    # ─────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("✓ Тестування паттерну Strategy завершено")
    print("=" * 70)
    print(f"\n📌 Для переключення стратегії встановіть змінну середовища:")
    print("   export OUTPUT_STRATEGY=console|kafka|file")
    print(f"\n📌 Поточна стратегія: {Config.OUTPUT_STRATEGY.upper()}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
