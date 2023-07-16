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
