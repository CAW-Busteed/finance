import os
import mylogic
import mydb
import pytest
from cs50 import SQL


@pytest.fixture
def dbfile():
    fn = 'finance-test.db'
    if os.path.exists(fn): os.unlink(fn)
    with open(fn, 'w') as f:
        pass  # create empty file


@pytest.fixture
def dbfixture(dbfile):

    cmds = [
        """CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);""",
        """CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, company TEXT NOT NULL, shares INTEGER NOT NULL DEFAULT 1, total_cost NUMERIC NOT NULL, type TEXT NOT NULL, date TEXT NOT NULL);""",
        """CREATE TABLE assets (user_id integer NOT NULL, stock text NOT NULL, number integer NOT NULL, value numeric NOT NULL, total_value numeric NOT NULL);"""
    ]
    db = SQL("sqlite:///finance-test.db")
    for cmd in cmds:
        db.execute(cmd)

    # create some test rows for each table with inserts.
    return db


def test_dostuff(dbfixture):
    import pdb
    pdb.set_trace()  # roy
    # assert dostuff(db, user_id)

def add_transactions(dbfixture, id, time, quote, shares, cost, type):
   dbfixture.execute("INSERT INTO transactions (user_id, date, company, shares, total_cost, type) VALUES (?, ?, ?, ?, ?, ?)",
              id, time, quote, shares, cost, type)

def test_get_transactions(dbfixture):
    user_id = 0
    add_transactions(dbfixture, user_id, '12:00', 'GOOG', 3, 123.45, 'buy')
    test_db = mydb.get_transactions(dbfixture, user_id)
    assert test_db[0]['stock']== 3