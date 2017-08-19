#!/usr/bin/env python
#Imports
from bittrex import bittrex
from time import sleep
import time
import sys
from poloniex import poloniex
def main(argv):
	period = float(raw_input("Period(Delay Between Each Check in seconds):	"))
	currency = raw_input("Coin(Example: ETH):	")
	minArb=float(raw_input("Minimum Arbitrage %. Recomended to set above 100.5 as fees from both sides add up to 0.5%.	"))
	trade = 'BTC'
	tradePlaced = False

	#Bittrex API Keys
	api = bittrex('BITTREXAPIKEYHERE','BITTREXAPISECRETHERE')

	#Bittrex market
	market= '{0}-{1}'.format(trade,currency)

	#Polo market
	pair= '{0}_{1}'.format(trade,currency)

	#Polo API Keys
	conn= poloniex('POLONIEXAPIKEY','POLONIEXAPISECRET')

	while True:
		#Poloniex Prices
		currentValues = conn.api_query("returnTicker")
		poloBid = float(currentValues[pair]["highestBid"])
		poloAsk = float(currentValues[pair]["lowestAsk"])
		print "Bid @ Poloniex:	" + str(poloBid)
		print "Ask @ Poloniex	" + str(poloAsk)

		#Bittrex Prices
		summary=api.getmarketsummary(market)
		bittrexAsk = summary[0]['Ask']
		print "Ask @ Bittrex:	" + str(bittrexAsk)
		bittrexBid = summary[0]['Bid']
		print "Bid @ Bittrex:	" + str(bittrexBid)

		#Balances for currency
		bittrexBalance=api.getbalance(currency)
		allpolobalance=conn.apiquery('returnBalances')
		poloniexBalance=allpolobalance[currency]


		#Balances for BTC
		bittrexBTCBalance=api.getbalance(btc)
		poloniexBTCBalance=allpolobalance[btc]


		if (poloAsk<bittrexBid):
			arbitrage=bittrexBid/poloAsk
			if ((arbitrage*100)>minArb):
				print "Buy from poloAsk, sell to bittrexBid. Profit: " + str(arbitrage*100)
				sellbook=conn.returnOrderBook(pair)["asks"][0][1]
				buybook=api.getorderbook(market, "sell")[0]["Quantity"]
				lowestbook=min(sellbook, buybook)
				#polocost=poloAsk*sellbook
				api.selllimit(market, lowestbook, bittrexBid)
				orderNumber=conn.sell(pair, poloAsk, lowestbook)
				print "Selling {0} {1} @ BittrexBid @ {2} and buying {3} {4} @ PoloAsk @ {5}".format(lowestbook, currency, bittrexBid, lowestbook, currency, poloAsk)

			#else:
			#print "Arbitrage found but less than min arb."
		elif(bittrexAsk<poloBid):
			arbitrage=poloBid/bittrexAsk
			if ((arbitrage*100)>minArb):
				print "Buy from Bittrex Ask, sell to poloBid. Profit: " + str(arbitrage*100)
				buybook=conn.returnOrderBook(pair)["bids"][0][1]
				sellbook=api.getorderbook(market, "sell")[0]["Quantity"]
				lowestbook=min(sellbook, buybook)
				api.buylimit(market, lowestbook, bittrexAsk)
				orderNumber=conn.sell(pair, poloBid, lowestbook)
				print "Selling {0} {1} @ PoloBid @ {2} and Buying {3} {4} @ BittrexAsk @ {5}".format(lowestbook, currency, poloBid, lowestbook, currency, bittrexAsk)

#			else:
#				print "Arbitrage found but less than min arb."
		time.sleep(period)


if __name__ == "__main__":
	main(sys.argv[1:])
