from kucoin.client import Client
from utils import calc_arb,round_down
import constants
import time
import random
from kucoin import exceptions


client = Client(constants.api_key, constants.api_secret, constants.api_passphrase)
symbols_list = client.get_symbols()

# ------------- FUNCTIONS -------------

''' Perform a triangular arbitrage trade on a set of currency pairs
    reverse is true when a reverse arbitrage is desired '''
def init_arb(tic1,tic2,tic3,reverse = False):   
    print("Start trade..")
    # buy first tic with tether
    usd_tic = f"{tic1.split('-')[0]}-USDT"
    # Purchase INIT_USDT worth of base pair (buying currency pair)
    trade_n_wait(usd_tic,client.SIDE_BUY,constants.INIT_USDT,_usdt = True)
    # Sell currency pair: Get previous base pair size and sell that as new base pair size
    trade_n_wait(tic1,client.SIDE_SELL)
    if not reverse:        
        trade_n_wait(tic2,client.SIDE_SELL)
    else:        
        trade_n_wait(tic2,client.SIDE_BUY)

    trade_n_wait(tic3,client.SIDE_BUY)
        
    final_deal = trade_n_wait(usd_tic,client.SIDE_SELL)

    print(f"Done! final USDT of {final_deal}")

''' creates an order for a currency pair (either BUY/SELL)
    waits until order is inactive to continue '''
def trade_n_wait(_symbol,_side,_usdt_amount = 0,_usdt = False):
    pairInfo = ticsInfo[_symbol]
    baseTic,quoteTic = _symbol.split("-")

    if _side == client.SIDE_BUY:
        tic = quoteTic
        dec = "quoteDecimal"
        deal = "dealSize"
    elif _side == client.SIDE_SELL:
        tic = baseTic
        dec = "baseDecimal"
        deal = "dealFunds"

    if _usdt :
        available = _usdt_amount
    else:
        available = float(client.get_accounts(currency=tic)[0]['available'])

    
    print(f"Atemping to sell {available} of {tic} ")
    # account for fees
    amount = str(round_down(available-(available*0.1/100),pairInfo[dec]))

    # attempt to purchase/sell currency
    while True:
        try:
            if _side == client.SIDE_BUY:
                order_id = client.create_market_order(symbol = _symbol,side = _side,funds = amount)['orderId']
            elif _side == client.SIDE_SELL:
                order_id = client.create_market_order(symbol = _symbol,side = _side,size = amount)['orderId']
            break
        # case when kucoin account hasnt synced yet
        except exceptions.KucoinAPIException as err:
            if str(err.code) == '200004':
                print(f"Insufficent Balance of amount {amount}...Trying again...")
            else:
                print(err)

    # wait until order has completed
    while True:
        print("Getting Account..")
        order_info = client.get_order(order_id)
        order_deal = order_info[deal]
        if not order_info['isActive']:
            break
    
    print(f"Sucessful {_symbol} trade, order_id = {order_id},order_deal = {order_deal}")
    return float(order_deal)

# function to get info about pair e.g BTC/ETH
def get_pair_info(symbol):
    info_list = list(filter(lambda x: x['symbol'] == symbol,symbols_list))
    if info_list == []:
        return []
    return info_list[0]

# This function takes in a list of tic pairs e.g [AAVE/USDT,..], returns a dictionary with info as value
def get_tics_info(tics):
    my_dict = dict()
    for tic in tics:
        my_dict[tic] = get_pair_info(tic)
        base,quote = tic.split("-")
        base_usdt = f"{base}-USDT"
        my_dict[base_usdt] = get_pair_info(base_usdt)
    return my_dict
    
# Select a list of currencys to test for arbitrages
def get_tics():
    # get list of symbol currency pairs and remove all the ones with stable coins
    symbols = list(filter(lambda sym:[el for el in sym.split("-") for stable in constants.STABLE_COINS if el == stable] == [],[x['symbol'] for x in symbols_list]))[:800]
    tics = []
    for a in symbols:
        a_base,a_quote = a.split("-")
        if len(get_pair_info(f"{a_base}-USDT")) == 0:
            continue
        for b in symbols:
            b_base,b_quote = b.split("-")
            if a_quote != b_base:
                continue
            for c in symbols:
                c_base,c_quote = c.split("-")
                # no stable coins and a_base has to be tradeable with usdt
                if a_base == c_base and b_quote == c_quote:
                    tics.append((a,b,c))
    return tics

# ------------- MAIN CODE -------------

# Testing IP address
client.get_accounts(currency='AAVE')
print("Ip address OK!")
tics = get_tics()
random.shuffle(tics)
flatten_tics = [item for tup in tics for item in tup]
ticsInfo = get_tics_info(flatten_tics)

# calculate the needed quote and base decimal increments
for currency_pair,info in ticsInfo.items():
    info['quoteDecimal'] = len(info['quoteIncrement'])-2
    info['baseDecimal'] = len(info['baseIncrement'])-2

print("Looking for trade!")
# keep checking arb value until tradable
while True:
    for tic in tics:
        tic1_info = client.get_ticker(tic[0])
        tic2_info = client.get_ticker(tic[1])
        tic3_info = client.get_ticker(tic[2])
        forward_arb = calc_arb(tic1_info,tic2_info,tic3_info)
        if forward_arb > constants.PRINT_TICS_THRESH:
            print(f"Forward Arb for {[tic[0],tic[1],tic[2]]} : {forward_arb}")

        if forward_arb > constants.ARB_THRESH:
            # start timer
            start = time.time()
            # initalise arbitrage trade between currency pairs
            init_arb(tic[0],tic[1],tic[2])
            print(f" Time to trade completed in {time.time()-start}")
            break

        # Reverse arbitrage trade between currency pairs
        reverse_arb = calc_arb(tic1_info,tic2_info,tic3_info,reverse=True)
        if reverse_arb > constants.PRINT_TICS_THRESH:
            print(f"Reverse Arb for {[tic[0],tic[1],tic[2]]} : {reverse_arb}")
        if reverse_arb > constants.ARB_THRESH:
            # start timer 
            start = time.time()
            init_arb(tic[2],tic[1],tic[0],reverse = True)
            print(f" Time to trade completed in {time.time()-start}")
            break

    time.sleep(constants.REFRESH_SEC)

