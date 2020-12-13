import unittest

import app
import testutil


class AppTest(testutil.DbTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_all_rows(self):
        dal = self.getDAL()
        with dal.get_connection() as conn:
            ins = dal.table.insert().values(id=1, name="TEST")
            conn.execute(ins)

        rows = app.get_all_rows(dal)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].name, "TEST")


if __name__ == '__main__':
    unittest.main()
