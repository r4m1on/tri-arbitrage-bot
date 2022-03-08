# tri-arbitrage-bot
Cryptocurrency trading bot that utilizes triangular arbitrage on the KuCoin exchange

The basic strategy around Triangular Arbitrage is to exploit the discrepency between three currencies for a profit. For example, if I trade all my Bitcoin for Ether which is then traded for ADA which is traded back to Bitcoin and I have more Bitcoin then what I started with, I have found a triangular arbitrage opportunity. The bot I have written has two different branches representing two slightly different strategies

### The Instant Bought Strategy 
This strategy randomly selects a few hundred groups of three currencies which have the potenital for arbitrage opportunities. The program then will scan through these groups and look for arbitrage opportunities. Once a group is found that meets the minimum profit requirement as predetermined by the user in constants.py, a trade will begin executing

### The Pre Bought Strategy
This strategy is similar to the instant bought one but differs in the way groups of coins are chosen to look for. The coins are chosen by analysing which currency's produce the most volatile discrepensies in several groups in which they are the starting coin over some time period. The top 3 or so coins that appear to be most likely to have future arbitrage opportunities are immediatley bought and are scanned a few times a second until some group meets a profit threshold, just like the previous strategy

### Program speed
Originally I had started with the instant bought strategy but found my program was too slow and by the time trading was done, opportunities had been gone and prices had changed. This motivated me to try pre buy coins and therefore reduce the total number of trades by one, because I would already have purchased the starting coin.

The fastest I could get the program to run from detecting a profit to executing all the trades was around *0.5* seconds on an AWS instance, unfortunately too slow and I wasn't able to make a profit in time.

## How to Run

1) Set the API Keys and secrets linking to your [KuCoin Account](https://www.kucoin.com/) which can be configured in the API management section of the website
2) Link these keys to corresponding variables in **constants.py**
3) Set appropriate values to variables in constants.py e.g _**ARB_THRESH**_ is used for the minimum percent profit required to trigger a trade on a currency trio
4) Run ```python trade.py``` (assuming you have python 3 installed)
