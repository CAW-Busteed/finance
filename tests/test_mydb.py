import os
import tempfile
import mydb
import pytest
from cs50 import SQL
from sqlalchemy.util import deprecations
from datetime import datetime

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


def test_dostuff(db):
    data, user_cash, gross_value = mydb.dostuff(db, user_id=1)
    assert data[1]['stock'] == 'GOOG'
    assert data[1]['value'] == 119.69
    assert user_cash[0]['cash'] == 3953.65
    assert gross_value[0]['total_value'] == 380.46

def test_buy_variables():
    stock_dic = {'price': 33.35}
    share_num = 3
    cost, time, buyorsell = mydb.buy_variables(stock_dic, share_num)
    assert float("{:.2f}".format(cost)) == 100.05

def test_buy_main(db):
    rows = db.execute("SELECT * FROM users WHERE id = ?", 1)
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    asset = mydb.buy_main(db, rows, 1, time, 'goog', 3, 100.05, 'buy')
    assert asset[0]['stock'] == 'GOOG'
    assert asset[0]['number'] == 3

def test_buy_update(db):
    asset = []
    stock_dic = {'price': 33.35}
    cost = 100.05
    test = mydb.buy_update(asset, db, 1, 'GOOG', 3, stock_dic, cost)
    assert test == True

def test_sell_variables(db):
    stock_dic = {'price': 33.35}
    rows, assets, cost, buyorsell, time = mydb.sell_variables(db, 1, 'GOOG', stock_dic, 3)

def test_sell_main(db):
    stock_dic = {'price': 33.35}
    total_value = stock_dic["price"] * 2
    test = mydb.sell_main(2, db, stock_dic, total_value, 1, 'GOOG')
    assert test == True

def test_sell_update(db):
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    cost = 33
    rows = db.execute("SELECT * FROM users WHERE id = ?", 1)
    gains = rows[0]["cash"] + cost
    test = mydb.sell_update(db, 1, gains, time, 'GOOG', 2, cost, 'sell')
    assert test == True