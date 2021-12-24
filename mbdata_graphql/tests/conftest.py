import pytest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import mbdata.config
mbdata.config.configure(schema=None)
mbdata.config.freeze()

from mbdata.models import Base  # noqa: E402


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def db_session(db_engine) -> Session:
    session = Session(bind=db_engine)
    return session
