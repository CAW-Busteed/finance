from helpers import apology, login_required, lookup, usd


def dostuff2(gross_value, user_cash):
    total = 0
    x = 0
    if gross_value == []:
        total = float(user_cash[0]["cash"])
    elif len(gross_value) == 1:
        total = gross_value[0]["total_value"] + user_cash[0]["cash"]
    else:
        while x < len(gross_value):
            total += gross_value[x]["total_value"]
            x += 1
        total += user_cash[0]["cash"]
    return total


def stockcheck1(stock_quote):
    if stock_quote.isalpha() == False:
        return apology("Invalid symbol")
    elif len(stock_quote) == 0:
        return apology("Invalid symbol")
    return True


def sharenum_check(share_num):
    if share_num.isdigit() == False:
        return apology("Invalid numbers")
    elif int(share_num) == ValueError:
        return apology("Whole numbers only")
    elif int(share_num) < 1:
        return apology("No stocks selected")


def norows(rows):
    if rows[0] == None:
        return apology("Database error")


def stockcheck2(stock_dic, cost, rows):
    if stock_dic == None:
        return apology("No stock of that code found", 400)
        #TODO:4- L/M set limits in the html itself
    elif cost > rows[0]["cash"]:
        return apology("Not enough money to purchase", 400)


def getquote(stock_quote):
    if len(stock_quote) == 0:
        return apology("No stock inputted")
    elif lookup(stock_quote) == None:
        return apology("No stock of that code found")
    else:
        stock_dic = lookup(stock_quote)
        return stock_dic


# def register():
#     if not request.form.get("username"):
#         return apology("must provide username")
#     elif not request.form.get("password"):
#         return apology("must provide password")
#     elif not request.form.get("confirmation"):
#         return apology("must provide confirmation")


def pass_compare(password1, password2):
    if password1 != password2:
        return apology("Passwords do not match")


def pass_parameters(password):
    if len(password) < 8:
        return apology(
            "Must provide a password at least 8 characters in length")


def username_avail(rows):
    if len(rows) > 0:
        return apology("username unavailable")


def symbol_check(stock_quote):
    if stock_quote.isalpha() == False:
        return apology("Invalid symbol")


def valid_form(share_num):
    if share_num.isdigit() == False:
        return apology("Invalid numbers")
    elif int(share_num) == ValueError:
        return apology("Whole numbers only")
    elif int(share_num) < 1:
        return apology("No stocks selected")


def error_catch(stock_dic, assets, share_num):
    if stock_dic == None:
        return apology("No stock of that code found")
    elif assets == None:
        return apology("Stock not found in portfolio")
    elif int(share_num) > assets[0]["number"]:
        return apology("Sold more stock than user possesses")
