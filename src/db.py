import threading

from sqlalchemy import MetaData, Table, Column, Integer, String, engine_from_config
from sqlalchemy.engine.base import Engine, Connection


class DataAccessLayer:
    __metadata = MetaData()
    table = Table(
        "table",
        __metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False)
    )

    def __init__(self, engine_config: dict):
        # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine
        assert engine_config, "Engine configuration must not be empty"
        self.__engine: Engine = engine_from_config(engine_config)
        self.__thread_local = threading.local()

    def _init_db(self):
        DataAccessLayer.__metadata.create_all(self.__engine)

    def get_connection(self) -> Connection:
        # no caching needed, since connections are pooled
        return self.__engine.connect()
