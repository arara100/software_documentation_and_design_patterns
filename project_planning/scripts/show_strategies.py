#!/usr/bin/env python3
"""
ЛР4: Показати всі стратегії виводу в одному запуску.

Демонструє роботу кожної стратегії без зміни ENV змінних.
Стратегії з зовнішніми сервісами (Kafka, Redis, Firebase)
показують архітектуру та перехоплюють відсутні залежності.

Запуск:
    python3 scripts/show_strategies.py
"""

import sys
import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from infrastructure.config import Config
from infrastructure.database import init_db, create_all_tables
from business_logic.strategies.console_output_strategy import ConsoleOutputStrategy
from business_logic.strategies.file_output_strategy import FileOutputStrategy

# ─── Тестові дані (спільні для всіх стратегій) ───────────────────────────────

SAMPLE_STATS = {
    "projects": 60,
    "tasks": 840,
    "resources": 250,
    "assignments": 1709,
}

SAMPLE_TASKS = [
    "Реалізувати REST API",
    "Написати модульні тести",
    "Налаштувати CI/CD",
    "Задокументувати код",
]

# ─── Хелпер для заголовків ────────────────────────────────────────────────────

def header(title: str, width: int = 70):
    print("\n" + "═" * width)
    print(f"  {title}")
    print("═" * width)

def sub(title: str):
    print(f"\n  ▶ {title}")
    print("  " + "─" * 50)

def result(ok: bool, msg: str):
    icon = "✅" if ok else "⚠️ "
    print(f"  {icon}  {msg}")


# ─── 1. CONSOLE ──────────────────────────────────────────────────────────────

def demo_console():
    header("Стратегія 1 — ConsoleOutputStrategy")
    print("  Вивід: stdout (термінал)")
    print("  Запуск: python3 scripts/test_output_strategy.py")
    sub("output(message)")

    s = ConsoleOutputStrategy()
    s.output("📂 Читання CSV файлу: data/data.csv")

    sub("output_dict(stats)")
    s.output_dict(SAMPLE_STATS)

    sub("output_list(tasks)")
    s.output_list(SAMPLE_TASKS)

    result(True, "ConsoleOutputStrategy — працює локально (без залежностей)")


# ─── 2. FILE ─────────────────────────────────────────────────────────────────

def demo_file():
    header("Стратегія 2 — FileOutputStrategy")
    file_path = os.path.join(PROJECT_ROOT, "output", "demo_show.jsonl")
    print(f"  Вивід: файл  →  output/demo_show.jsonl")
    print("  Запуск: OUTPUT_STRATEGY=file python3 scripts/test_output_strategy.py")
    sub("output_dict(stats) + output_list(tasks)")

    s = FileOutputStrategy(file_path=file_path)
    s.output("📂 Читання CSV файлу: data/data.csv")
    s.output_dict(SAMPLE_STATS)
    s.output_list(SAMPLE_TASKS)
    s.flush()

    # Показати вміст файлу
    sub("Вміст записаного файлу (JSONL):")
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            obj = json.loads(line)
            ts = obj.get("timestamp", "")[:19]
            t = obj.get("type", "")
            if t == "statistics":
                preview = str(obj.get("data", {}))
            elif t == "list":
                preview = str(obj.get("items", []))
            else:
                preview = obj.get("message", "")[:60]
            print(f"  [{ts}] [{t:>12}]  {preview}")
    except Exception as e:
        print(f"  ❌ Помилка читання файлу: {e}")

    result(True, f"FileOutputStrategy — файл записано: {file_path}")


# ─── 3. KAFKA ────────────────────────────────────────────────────────────────

def demo_kafka():
    header("Стратегія 3 — KafkaOutputStrategy")
    print(f"  Вивід: Apache Kafka  →  topic: {Config.KAFKA_TOPIC}")
    print(f"  Broker: {Config.KAFKA_BOOTSTRAP_SERVERS}")
    print("  Запуск: OUTPUT_STRATEGY=kafka python3 scripts/test_output_strategy.py")

    sub("Спроба підключення...")
    try:
        from business_logic.strategies.kafka_output_strategy import KafkaOutputStrategy
        s = KafkaOutputStrategy(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            topic=Config.KAFKA_TOPIC,
        )
        s.output_dict(SAMPLE_STATS)
        s.flush()
        result(True, "KafkaOutputStrategy — повідомлення відправлено в Kafka")
    except ImportError:
        result(False, "kafka-python не встановлено → pip install kafka-python")
        _show_kafka_payload()
    except RuntimeError as e:
        result(False, f"Kafka недоступна (сервер не запущений): {e}")
        _show_kafka_payload()


def _show_kafka_payload():
    import json as _json
    from datetime import datetime
    payload = {
        "timestamp": datetime.now().isoformat(),
        "type": "statistics",
        "data": SAMPLE_STATS,
    }
    print("\n  Payload який буде відправлено в Kafka:")
    print("  " + _json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", "\n  "))


# ─── 4. REDIS ────────────────────────────────────────────────────────────────

def demo_redis():
    header("Стратегія 4 — RedisOutputStrategy")
    print(f"  Вивід: Redis  →  {Config.REDIS_HOST}:{Config.REDIS_PORT}")
    print(f"  Режим: {Config.REDIS_MODE}  |  Канал/ключ: {Config.REDIS_CHANNEL}")
    print("  Запуск: OUTPUT_STRATEGY=redis python3 scripts/test_output_strategy.py")
    print("  List-режим: REDIS_MODE=list OUTPUT_STRATEGY=redis python3 scripts/test_output_strategy.py")

    sub("Спроба підключення...")
    try:
        from business_logic.strategies.redis_output_strategy import RedisOutputStrategy
        s = RedisOutputStrategy(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=Config.REDIS_DB,
            channel=Config.REDIS_CHANNEL,
            mode=Config.REDIS_MODE,
        )
        s.output_dict(SAMPLE_STATS)
        s.output_list(SAMPLE_TASKS)
        s.flush()
        result(True, "RedisOutputStrategy — повідомлення відправлено в Redis")
    except ImportError:
        result(False, "redis не встановлено → pip install redis")
        _show_redis_payload()
    except RuntimeError as e:
        result(False, f"Redis недоступний (сервер не запущений): {e}")
        _show_redis_payload()


def _show_redis_payload():
    import json as _json
    from datetime import datetime
    payload = {
        "timestamp": datetime.now().isoformat(),
        "type": "statistics",
        "data": SAMPLE_STATS,
    }
    print("\n  Payload який буде відправлено в Redis:")
    mode_desc = {
        "pubsub": "PUBLISH data-output <payload>   ← pub/sub, real-time",
        "list":   "RPUSH  data-output <payload>   ← persistent queue/log",
    }
    print(f"  Команда Redis: {mode_desc.get(Config.REDIS_MODE, Config.REDIS_MODE)}")
    print("  " + _json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", "\n  "))


# ─── 5. FIREBASE ─────────────────────────────────────────────────────────────

def demo_firebase():
    header("Стратегія 5 — FirebaseOutputStrategy")
    print(f"  Вивід: Firebase Realtime DB  →  /{Config.FIREBASE_DB_PATH}")
    print(f"  URL: {Config.FIREBASE_DATABASE_URL or '(не задано, встановіть FIREBASE_DATABASE_URL)'}")
    print("  Запуск:")
    print("    FIREBASE_DATABASE_URL=https://<project>.firebaseio.com \\")
    print("    FIREBASE_CREDENTIALS_PATH=firebase-credentials.json \\")
    print("    OUTPUT_STRATEGY=firebase python3 scripts/test_output_strategy.py")

    sub("Спроба підключення...")
    try:
        from business_logic.strategies.firebase_output_strategy import FirebaseOutputStrategy
        if not Config.FIREBASE_DATABASE_URL:
            raise RuntimeError("FIREBASE_DATABASE_URL не встановлено")
        s = FirebaseOutputStrategy(
            credentials_path=Config.FIREBASE_CREDENTIALS_PATH,
            database_url=Config.FIREBASE_DATABASE_URL,
            db_path=Config.FIREBASE_DB_PATH,
        )
        s.output_dict(SAMPLE_STATS)
        s.output_list(SAMPLE_TASKS)
        s.flush()
        result(True, "FirebaseOutputStrategy — дані записано в Firebase")
    except ImportError:
        result(False, "firebase-admin не встановлено → pip install firebase-admin")
        _show_firebase_payload()
    except RuntimeError as e:
        result(False, f"Firebase недоступний: {e}")
        _show_firebase_payload()


def _show_firebase_payload():
    import json as _json
    from datetime import datetime
    payload = {
        "timestamp": datetime.now().isoformat(),
        "type": "statistics",
        "data": SAMPLE_STATS,
    }
    print("\n  Структура в Firebase Realtime Database:")
    print(f"  /{Config.FIREBASE_DB_PATH}/")
    print("    <auto-push-key>/")
    print("  " + _json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", "\n  "))


# ─── ПІДСУМОК ─────────────────────────────────────────────────────────────────

def summary():
    header("Підсумок: всі стратегії паттерну Strategy")
    rows = [
        ("console",  "ConsoleOutputStrategy",  "stdout",              "без залежностей",  "✅ local"),
        ("file",     "FileOutputStrategy",     "JSONL файл",          "без залежностей",  "✅ local"),
        ("kafka",    "KafkaOutputStrategy",    "Apache Kafka",        "kafka-python",     "🐳 docker"),
        ("redis",    "RedisOutputStrategy",    "Redis pub/sub + list","redis",            "🐳 docker"),
        ("firebase", "FirebaseOutputStrategy", "Firebase Realtime DB","firebase-admin",   "☁️  cloud"),
    ]
    print(f"\n  {'ENV':10} {'Клас':30} {'Ціль':22} {'pip пакет':15} {'Оточення'}")
    print("  " + "─" * 90)
    for env, cls, target, dep, env_type in rows:
        print(f"  {env:10} {cls:30} {target:22} {dep:15} {env_type}")

    print(f"""
  Переключення без змін у коді:
    OUTPUT_STRATEGY=console   python3 scripts/test_output_strategy.py
    OUTPUT_STRATEGY=file      python3 scripts/test_output_strategy.py
    OUTPUT_STRATEGY=kafka     python3 scripts/test_output_strategy.py
    OUTPUT_STRATEGY=redis     python3 scripts/test_output_strategy.py
    OUTPUT_STRATEGY=firebase  python3 scripts/test_output_strategy.py
""")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db(Config.DATABASE_URL)
    create_all_tables()

    header("ЛР4 — GoF-паттерн Strategy: демонстрація всіх стратегій")

    demo_console()
    demo_file()
    demo_kafka()
    demo_redis()
    demo_firebase()
    summary()
