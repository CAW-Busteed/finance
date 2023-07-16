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
    
