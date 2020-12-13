import logging
import threading
import time

import sqlalchemy

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt=None
)

LOGGER = logging.getLogger(__name__)


def thread_function():
    with engine.connect() as connection:
        LOGGER.info("Connection: %s", connection.connection)
        time.sleep(1)


if __name__ == "__main__":
    # Explicit pooling strategy is necessary, because SQLite-in-memory
    # prohibits threading by default
    # https://www.kite.com/python/docs/sqlalchemy.dialects.sqlite.pysqlite
    engine = sqlalchemy.create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        echo=False,
        pool_size=3,
        max_overflow=0,
        poolclass=sqlalchemy.pool.QueuePool
    )

    metadata = sqlalchemy.MetaData()
    users = sqlalchemy.Table(
        'users',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String),
        sqlalchemy.Column('fullname', sqlalchemy.String)
    )

    addresses = sqlalchemy.Table(
        'addresses',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('user_id', None, sqlalchemy.ForeignKey('users.id')),
        sqlalchemy.Column('email_address', sqlalchemy.String, nullable=False)
    )

    metadata.create_all(engine)

    threads = []

    for x in range(10):
        t = threading.Thread(target=thread_function)
        threads.append(t)
        t.start()
        time.sleep(0.1)

    for t in threads:
        t.join()
