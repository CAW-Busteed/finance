import os
import mydb
import pytest
from cs50 import SQL
from sqlalchemy.util import deprecations

TEST_DB_FILENAME = 'finance-test.db'

# get rid of gratuitous warning from sqlAlchemy
deprecations.SILENCE_UBER_WARNING = True


@pytest.fixture
def dbfile(fn=TEST_DB_FILENAME):
    if os.path.exists(fn): os.unlink(fn)
    with open(fn, 'w') as f:
        pass  # create empty file
    return fn


@pytest.fixture
def db(dbfile):
    db = SQL(f"sqlite:///{dbfile}")

    def exec_script(sqlFile):
        with open(os.path.join(os.path.dirname(__file__), sqlFile), "r") as f:
            for line in f.readlines():
                if not line.strip(): continue  # skip empty lines
                db.execute(line)

    # populate_db
    exec_script("schema.sql")
    exec_script("data.sql")

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
