from typing import Generator

import pytest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import mbdata.config

mbdata.config.configure(schema=None)
mbdata.config.freeze()

from mbdata.models import Base  # noqa: E402
from mbdata.sample_data import create_sample_data  # noqa: E402


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine, None, None]:
    engine = create_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        session = Session(bind=engine)
        try:
            create_sample_data(session)
            session.commit()
        finally:
            session.close()
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def db_session(db_engine) -> Generator[Session, None, None]:
    try:
        session = Session(bind=db_engine)
        yield session
    finally:
        session.close()
