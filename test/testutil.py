import unittest

import db


class DbTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dal: db.DataAccessLayer = None

    def setUp(self) -> None:
        config = {
            "sqlalchemy.url": "sqlite:///:memory:",
            "sqlalchemy.echo": True,
            "sqlalchemy.hide_parameters": False
        }
        dal = db.DataAccessLayer(
            engine_config=config
        )
        dal._init_db()
        self.__dal = dal

    def tearDown(self) -> None:
        self.__dal = None

    def getDAL(self) -> db.DataAccessLayer:
        return self.__dal
