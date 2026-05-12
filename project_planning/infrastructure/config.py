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

    # ------------------------------------------------------------------ #
    # Output strategy configuration (Strategy pattern — Lab 4)           #
    # Set OUTPUT_STRATEGY=kafka to route output to Kafka instead of       #
    # stdout. All other keys are required only when kafka is selected.    #
    # ------------------------------------------------------------------ #
    OUTPUT_STRATEGY: str = os.getenv("OUTPUT_STRATEGY", "console")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "project_planning_output")
