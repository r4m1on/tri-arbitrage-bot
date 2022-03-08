from kucoin.client import Client
import constants
import time 
from utils import calc_arb

client = Client(constants.api_key, constants.api_secret, constants.api_passphrase)

# takes in a list of length 3 lists representing currency pairs
# returns a list of a_base pairs, containing the top 4 a_base pair currencies
def find_tics(tics):
    # dictionary counts number 
    count_dict = dict()
    start = time.time()
    while True:
        for tic in tics:
            tic1_info = client.get_ticker(tic[0])
            tic2_info = client.get_ticker(tic[1])
            tic3_info = client.get_ticker(tic[2])
            forward_arb = calc_arb(tic1_info,tic2_info,tic3_info)
            reverse_arb = calc_arb(tic1_info,tic2_info,tic3_info,reverse=True)
            a_base  = tic[0].split("-")[0]
            if a_base not in count_dict.keys():
                count_dict[a_base] = 0

            if forward_arb > constants.FIND_TICS_THRESH:
                count_dict[a_base] += 1

            if reverse_arb > constants.FIND_TICS_THRESH:
                count_dict[a_base] += 1
        # time to stop searching for possible a_bases
        if time.time() - start > constants.FIND_TICS_TIME:
            break
    tup_list = count_dict.items()
    sorted_list = sorted(tup_list,key = lambda tup:tup[1],reverse=True)
    return list(map(lambda tup:tup[0],sorted_list))[:constants.TOP_CURRENCY_AMOUNT]
    
    
# filter out the tickers in that arent in a_bases
def filter_tics(tics,a_bases):
    # see if a base in a_bases
    return list(filter(lambda tri:tri[0].split("-")[0] in a_bases,tics))