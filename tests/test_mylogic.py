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
