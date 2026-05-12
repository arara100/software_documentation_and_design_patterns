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
