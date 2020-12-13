from sqlalchemy import sql

import db


def main():
    config = {
        "sqlalchemy.url": "sqlite:///prod.db",
        "sqlalchemy.echo": False,
        "sqlalchemy.hide_parameters": True
    }
    dal = db.DataAccessLayer(config)
    rows = get_all_rows(dal)

    for row in rows:
        print(row)


def get_all_rows(dal: db.DataAccessLayer) -> list:
    with dal.get_connection() as conn:
        return conn.execute(sql.select([dal.table])).fetchall()


if __name__ == '__main__':
    main()
