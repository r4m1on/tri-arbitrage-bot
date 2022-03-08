import math

# gets the percent profit of tri-arbitrage with no transaction fees
def calc_arb(a_info,b_info,c_info,reverse=False):
    # FORMAT OF PAIRS : "AAVE-KCS","KCS-BTC","AAVE-BTC"
    if reverse:
        ratio = float(c_info['bestBid'])*1/float(b_info['bestAsk'])*1/float(a_info['bestAsk'])
    else:
        ratio = float(a_info['bestBid'])*float(b_info['bestBid'])*1/float(c_info['bestAsk'])
    return (ratio-1)*100

# Returns a value rounded down to a specific number of decimal places.
def round_down(number:float, decimals:int=2):
    if decimals == 0:
        return math.floor(number)
    multi = 10 ** decimals
    return math.floor(number * multi) / multi
