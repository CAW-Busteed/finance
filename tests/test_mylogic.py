import mylogic

# def test_dostuff2():
#     res = mylogic.dostuff2(gross_value=10,
#                            user_cash=[{
#                                'cash': 20
#                            }, {
#                                'cash': 30
#                            }])
#     assert res == 1


def test_stockcheck1():
    assert mylogic.stockcheck1(stock_quote="xx") == True

def test_sharenum_check():
    assert mylogic.sharenum_check('3') == True

def test_norows():
    rows = [1, 2, 3]
    assert mylogic.norows(rows) == True

def test_stockcheck2():
    stock_dic = {'change': '31', 'user': 1}
    cost = 60
    rows = [{'cash':61}]
    assert mylogic.stockcheck2(stock_dic, cost, rows) == True

def test_getquote():
    assert mylogic.getquote('goog') != None

def test_pass_compare():
    x = 'TRAFlike'
    y = 'TRAFlike'
    assert mylogic.pass_compare(x,y) == True

def test_pass_parameters():
    password = "password"
    assert mylogic.pass_parameters(password) == True

def test_username_avail():
    rows = []
    assert mylogic.username_avail(rows) == True

def test_symbol_check():
    assert mylogic.symbol_check("Grum") == True

def test_error_catch():
    stock_dic = {'change': '31', 'user': 1}
    assets = [{'number': 50}]
    share_num = '25'
    assert mylogic.error_catch(stock_dic, assets, share_num) == True