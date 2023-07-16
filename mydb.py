from datetime import datetime

def dostuff(db, user_id):
    data = db.execute("SELECT * FROM assets WHERE user_id = ?", user_id)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    gross_value = db.execute(
        "SELECT total_value FROM assets WHERE user_id = ?", user_id)
    return data, user_cash, gross_value

def rows(db, user_id):
    db.execute("SELECT * FROM users WHERE id = ?",
                          user_id)

def buy_variables(stock_dic, share_num):
    cost = stock_dic["price"] * float(share_num)
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    buyorsell = "buy"
    return cost, time, buyorsell

def buy_main(db, rows, user_id, time, stock_quote, share_num, cost, buyorsell):
    remainder = rows[0]["cash"] - cost
    db.execute("UPDATE users SET cash=? WHERE id = ?", remainder,
                user_id)
    db.execute(
        "INSERT INTO transactions (user_id, date, company, shares, total_cost, type) VALUES (?, ?, ?, ?, ?, ?)",
        user_id, str(time), stock_quote.upper(), share_num,
        cost, buyorsell)
    asset = db.execute(
        "SELECT * FROM assets WHERE user_id = ? AND stock = ?",
        user_id, stock_quote.upper())
    
    return asset

def buy_update(asset, db, user_id, stock_quote, share_num, stock_dic, cost):
    if len(asset) == 0:
        db.execute(
            "INSERT INTO assets (user_id, stock, number, value, total_value) VALUES (?, ?, ?, ?, ?)",
            user_id, stock_quote.upper(), share_num,
            stock_dic["price"], cost)
    else:
        number = asset[0]['number'] + int(share_num)
        total_value = stock_dic["price"] * number
        db.execute(
            "UPDATE assets SET number = ?, value = ?, total_value = ? WHERE user_id = ? and stock = ?",
            number, stock_dic["price"], total_value,
            user_id, stock_quote.upper())
        
def get_transactions(db, user_id):
    db.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY id",
            user_id)