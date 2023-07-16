def dostuff(db, user_id):
    data = db.execute("SELECT * FROM assets WHERE user_id = ?", user_id)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    gross_value = db.execute(
        "SELECT total_value FROM assets WHERE user_id = ?", user_id)
    return data, user_cash, gross_value
