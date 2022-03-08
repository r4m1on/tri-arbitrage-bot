import math

# gets the percent profit of tri-arbitrage with no transaction fees
def calc_arb(a_info,b_info,c_info,reverse=False):
    # "AAVE-KCS","KCS-BTC","AAVE-BTC"
    if reverse:
        ratio = float(c_info['bestBid'])*1/float(b_info['bestAsk'])*1/float(a_info['bestAsk'])
    else:
        ratio = float(a_info['bestBid'])*float(b_info['bestBid'])*1/float(c_info['bestAsk'])
    return (ratio-1)*100

# taken from https://kodify.net/python/math/round-decimals/#example-round-decimal-digits-up-and-down

def round_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor
