import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
     """Show portfolio of stocks"""
    # User reached route via GET
     if request.method == "GET":
        data = db.execute("SELECT * FROM assets WHERE user_id = ?", session["user_id"])
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        gross_value = db.execute("SELECT total_value FROM assets WHERE user_id = ?", session["user_id"])
        total = 0
        x=0
        if gross_value == []:
            total = float(user_cash[0]["cash"])
        elif len(gross_value) == 1:
            total = gross_value[0]["total_value"] + user_cash[0]["cash"]
        else:
            while x < len(gross_value):
                total += gross_value[x]["total_value"]
                x += 1
            total += user_cash[0]["cash"]
        return render_template("index.html", data = data, cash=usd(user_cash[0]["cash"]), sum= usd(total))
     #Else: where the sell all stock button would work


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock_quote = request.form.get("symbol")

        #check for errors
        if stock_quote.isalpha() == False:
            return apology("Invalid symbol")
        elif len(stock_quote) == 0:
            return apology("Invalid symbol")

        #acquire stock info, number of shares, the db, the cost
        stock_dic = lookup(stock_quote)
        share_num = request.form.get("shares")

        if share_num.isdigit() == False:
            return apology("Invalid numbers")
        elif int(share_num) == ValueError:
            return apology("Whole numbers only")
        elif int(share_num) < 1:
            return apology("No stocks selected")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if rows[0] ==None:
            return apology("Database error")

        cost = stock_dic["price"] * float(share_num) #float defaults
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        buyorsell = "buy"

        #account for misspell of stock and not enough funds
        if stock_dic == None:
            return apology("No stock of that code found", 400)
            #TODO:4- L/M set limits in the html itself
        elif cost > rows[0]["cash"]:
            return apology("Not enough money to purchase", 400)
        else:
            remainder = rows[0]["cash"] - cost
            db.execute("UPDATE users SET cash=? WHERE id = ?", remainder, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, date, company, shares, total_cost, type) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], str(time), stock_quote.upper(), share_num, cost, buyorsell)
            asset = db.execute("SELECT * FROM assets WHERE user_id = ? AND stock = ?", session["user_id"], stock_quote.upper())
            if len(asset) == 0:
                db.execute("INSERT INTO assets (user_id, stock, number, value, total_value) VALUES (?, ?, ?, ?, ?)", session["user_id"], stock_quote.upper(), share_num, stock_dic["price"], cost)
            else:
                number= asset[0]['number'] + int(share_num)
                total_value= stock_dic["price"] * number
                db.execute("UPDATE assets SET number = ?, value = ?, total_value = ? WHERE user_id = ? and stock = ?", number, stock_dic["price"], total_value, session["user_id"], stock_quote.upper())
            return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY id", session["user_id"])
        return render_template("history.html", transactions=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock_quote = request.form.get("symbol")
        if len(stock_quote)==0:
            return apology("No stock inputted")
        elif lookup(stock_quote) == None:
            return apology("No stock of that code found")
        else:
            stock_dic = lookup(stock_quote)
            return render_template("quoted.html", name= stock_dic["name"], symbol= stock_dic["symbol"], price= usd(stock_dic["price"]))

     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        # Ensure passwords were long enough and accurate
        password1, password2 = request.form.get("password"), request.form.get("confirmation")


        if password1 != password2:
            return apology("Passwords do not match")
        # elif len(password1) < 8:
        #     return apology("Must provide a password at least 8 characters in length", 400)

        # Query database for username availability
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username unavailable")

        #input user data in user table and login
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        #user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        stock_quote = request.form.get("symbol").upper()

        #check for malignant errors
        if stock_quote.isalpha() == False:
            return apology("Invalid symbol")

        stock_dic = lookup(stock_quote)
        share_num = request.form.get("shares")

        if share_num.isdigit() == False:
            return apology("Invalid numbers")
        elif int(share_num) == ValueError:
            return apology("Whole numbers only")
        elif int(share_num) < 1:
            return apology("No stocks selected")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        assets = db.execute("SELECT * FROM assets WHERE user_id = ? AND stock = ?", session["user_id"], stock_quote.upper())
        cost = stock_dic["price"] * float(share_num)
        buyorsell= "sell"
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

        #account for misspell of stock and nonexistence in portfolio
        if stock_dic == None:
            return apology("No stock of that code found")
        elif assets == None:
            return apology("Stock not found in portfolio")
        elif int(share_num) > assets[0]["number"]:
            return apology("Sold more stock than user possesses")
        #TODO:4- L/M set limits in the html itself
        else:
            gains = rows[0]["cash"] + cost
            number= assets[0]["number"] - int(share_num)
            total_value= stock_dic["price"] * number

            #delete fromassets if there are some stocks left.
            if number > 0:
                db.execute("UPDATE assets SET number = ?, value = ?, total_value = ? WHERE user_id = ? AND stock = ?", number, stock_dic["price"], total_value, session["user_id"], stock_quote.upper())
            else:
                db.execute("DELETE FROM assets WHERE user_id = ? AND stock = ?", session["user_id"], stock_quote.upper())

            #update cash and history
            db.execute("UPDATE users SET cash=? WHERE id = ?", gains, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, date, company, shares, total_cost, type) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], time, stock_quote.upper(), share_num, cost, buyorsell)
            return redirect("/")
    else:
        return render_template("sell.html")
