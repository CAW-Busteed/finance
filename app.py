import os


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import mydb
import mylogic

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
        data, user_cash, gross_value = mydb.dostuff(db, session['user_id'])
        total = mylogic.dostuff2(gross_value, user_cash)
        return render_template("index.html",
                               data=data,
                               cash=usd(user_cash[0]["cash"]),
                               sum=usd(total))
    #Else: where the sell all stock button would work


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock_quote = request.form.get("symbol")

        #check for errors
        mylogic.stockcheck1(stock_quote)

        #acquire stock info, number of shares, the db, the cost
        stock_dic = lookup(stock_quote)
        share_num = request.form.get("shares")

        #check for errors in number of shares
        mylogic.sharenum_check(share_num)

        #define database
        rows = mydb.rows(db, session["user_id"])
        
        #check db if exists
        mylogic.norows(rows)

        cost, time, buyorsell = mydb.buy_variables(stock_dic, share_num)

        #account for misspell of stock and not enough funds
        mylogic.stockcheck2(stock_dic, cost, rows)

        #calculate assets
        asset = mydb.buy_main(db, rows, session["user_id"], time, stock_quote, share_num, cost, buyorsell)
        
        #update db
        mydb.buy_update(asset, db, session["user_id"], stock_quote, share_num, stock_dic, cost)
        
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        transactions = mydb.get_transactions(db, session["user_id"])
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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")):
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
        stock_dic = mylogic.getquote(stock_quote)
        return render_template("quoted.html",
                                name=stock_dic["name"],
                                symbol=stock_dic["symbol"],
                                price=usd(stock_dic["price"]))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure fields were submitted
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")
        
        # Ensure passwords were long enough and accurate
        password1, password2, username = request.form.get("password"), request.form.get(
            "confirmation"), request.form.get("username")
        mylogic.pass_compare(password1, password2)
        #mylogic.pass_parameters(password1)

        # Query database for username availability
        rows = mydb.rows(db, username)
        mylogic.username_avail(rows)

        #input user data in user table
        hash_pass = generate_password_hash(password1)
        mydb.user_input(db, username, hash_pass)

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
        mylogic.symbol_check(stock_quote)

        stock_dic = lookup(stock_quote)
        share_num = request.form.get("shares")
        mylogic.valid_form(share_num)

        rows, assets, cost, buyorsell, time = mydb.sell_variables(db, session["user_id"], stock_quote, stock_dic, share_num)

        #account for misspell of stock and nonexistence in portfolio
        mylogic.error_catch(stock_dic, assets, share_num)
        
        gains = rows[0]["cash"] + cost
        number = assets[0]["number"] - int(share_num)
        total_value = stock_dic["price"] * number

        #delete from assets if there are some stocks left.
        mydb.sell_main(number, db, stock_dic, total_value, session["user_id"], stock_quote)

        #update cash and history
        mydb.sell_update(db, session["user_id"], gains, time, stock_quote, share_num, cost, buyorsell)
        return redirect("/")
    else:
        return render_template("sell.html")
