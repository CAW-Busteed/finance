import os
import tempfile
import mydb
import pytest
from cs50 import SQL
from sqlalchemy.util import deprecations

# get rid of gratuitous warning from sqlAlchemy
deprecations.SILENCE_UBER_WARNING = True


@pytest.fixture(scope="session")
def dbfile():
    db_fd, db_path = tempfile.mkstemp()

    yield db_path

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="session")
def db(dbfile):
    db = SQL(f"sqlite:///{dbfile}")

    def exec_script(sqlFile):
        with open(os.path.join(os.path.dirname(__file__), sqlFile), "r") as f:
            for line in f.readlines():
                if not line.strip(): continue  # skip empty lines
                db.execute(line)

    exec_script("schema.sql")  # create tables
    exec_script("data.sql")  # populate_db

    return db


# test seeded db.
def test_get_transactions(db):
    # test_db = mydb.get_users(db, user_id=1)
    # assert test_db[0]['shares'] == 6
    # test_db = mydb.get_assets(db, user_id=1)
    # assert test_db[0]['shares'] == 6
    test_db = mydb.get_transactions(db, user_id=1)
    assert test_db[0]['shares'] == 6


# def test_dostuff(dbfixture):
#     add_transactions(dbfixture, user_id, '12:00', 'GOOG', 3, 123.45, 'buy')
#     assert mydb.dostuff(dbfixture, user_id=0)

# def add_transactions(dbfixture, id, time, quote, shares, cost, type):
#     dbfixture.execute(
#         "INSERT INTO transactions (user_id, date, company, shares, total_cost, type) VALUES (?, ?, ?, ?, ?, ?)",
#         id, time, quote, shares, cost, type)
