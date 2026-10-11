from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """Engine for the test database, with a fresh schema built once per test run."""
    # Imported here so tests that don't need a database run without any settings.
    import app.models  # noqa: F401  registers models on Base.metadata
    from app.core.config import settings
    from app.core.database import Base

    test_url = settings.TEST_DATABASE_URL
    if test_url is None:
        pytest.exit("TEST_DATABASE_URL is not set; refusing to run database tests.", returncode=2)
    url = make_url(test_url)
    # Safety guard: these tests drop every table, so never let them near the dev database.
    if test_url == settings.DATABASE_URL or not (url.database or "").endswith("_test"):
        pytest.exit(f"Refusing to run: '{url.database}' does not look like a test database.", returncode=2)

    _create_database_if_missing(url.database or "", url.set(database="postgres"))

    engine = create_engine(test_url, pool_pre_ping=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def _create_database_if_missing(name: str, admin_url: object) -> None:
    # CREATE DATABASE cannot run inside a transaction, hence AUTOCOMMIT.
    admin = create_engine(admin_url, isolation_level="AUTOCOMMIT")  # type: ignore[arg-type]
    with admin.connect() as conn:
        exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": name}).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{name}"'))
    admin.dispose()
