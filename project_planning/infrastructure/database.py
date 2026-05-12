from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Optional


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def init_db(database_url: str):
    global _engine, _SessionLocal
    _engine = create_engine(database_url, echo=False, connect_args={"check_same_thread": False})
    _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    return _engine


def get_engine():
    return _engine


def get_session() -> Session:
    return _SessionLocal()


def create_all_tables() -> None:
    # Import all models so SQLAlchemy registers them with Base.metadata
    from data_access.models import project_model  # noqa: F401
    from data_access.models import task_model      # noqa: F401
    from data_access.models import resource_model  # noqa: F401
    Base.metadata.create_all(_engine)
