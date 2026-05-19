from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL, future=True)
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

    db_path = Path(settings.DUCKDB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS costs (
                id INTEGER,
                service VARCHAR,
                monthly_cost DOUBLE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER,
                name VARCHAR,
                resource_type VARCHAR,
                monthly_cost DOUBLE
            )
            """
        )


def _init_postgres() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS costs (
                    id SERIAL PRIMARY KEY,
                    service VARCHAR(255) NOT NULL,
                    monthly_cost DOUBLE PRECISION NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS resources (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    resource_type VARCHAR(255) NOT NULL,
                    monthly_cost DOUBLE PRECISION NOT NULL
                )
                """
            )
        )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _init_duckdb()
    try:
        _init_postgres()
    except Exception:
        # Allow app startup in environments where Postgres is unavailable.
        pass
