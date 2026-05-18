from sqlalchemy import create_engine
from pathlib import Path
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from api.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _init_duckdb() -> None:
    try:
        import duckdb  # type: ignore
    except Exception:
        return

    db_path = Path(settings.duckdb_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cost_snapshots (
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                provider VARCHAR,
                service VARCHAR,
                cost DOUBLE
            )
            """
        )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _init_duckdb()
