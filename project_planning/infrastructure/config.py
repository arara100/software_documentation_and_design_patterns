import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)


class Config:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(PROJECT_ROOT, 'data', 'project_planning.db')}",
    )
    CSV_FILE_PATH: str = os.getenv(
        "CSV_FILE_PATH",
        os.path.join(PROJECT_ROOT, "data", "data.csv"),
    )
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    TESTING: bool = False
    
    # ================================================================
    # Output Strategy Configuration (ЛР4 Strategy Pattern)
    # ================================================================
    # Дозволені стратегії: "console", "kafka", "file", "redis", "firebase"
    # Значення за замовчуванням: "console"
    # Приклад: OUTPUT_STRATEGY=redis python app.py
    OUTPUT_STRATEGY: str = os.getenv("OUTPUT_STRATEGY", "console").lower()

    # Kafka configuration
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "data-output")

    # File output configuration
    OUTPUT_FILE_PATH: str = os.getenv(
        "OUTPUT_FILE_PATH",
        os.path.join(PROJECT_ROOT, "output", "log.jsonl"),
    )

    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_CHANNEL: str = os.getenv("REDIS_CHANNEL", "data-output")
    REDIS_MODE: str = os.getenv("REDIS_MODE", "pubsub")  # "pubsub" or "list"

    # Firebase configuration
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        os.path.join(PROJECT_ROOT, "firebase-credentials.json"),
    )
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", "")
    FIREBASE_DB_PATH: str = os.getenv("FIREBASE_DB_PATH", "output-logs")
