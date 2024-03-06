from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
    declarative_base,
)
from sqlalchemy.pool import StaticPool

import config


Base = declarative_base()


class Database:

    def __init__(self):
        self.url = config.DATABASE_URL
        self._create_engine()
        self._create_database()

    def _create_engine(self) -> None:
        """
        https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
        """
        self.engine = create_engine(
            self.url,
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )

    def _create_database(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def _session_factory(self) -> Type[Session]:
        """
        The purpose of sessionmaker is to provide a factory
        for Session classes with a fixed configuration.
        """
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def session(self) -> Session:
        return self._session_factory()()
