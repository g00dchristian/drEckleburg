from bnWebsocket.klines import bnStream
from bnWebsocket.languageHandled import languageHandler
import slack
import keychain
import ccxt
import time




class Eckleburg():
	def __init__(self, pairs, timeFrame):
		self.movement=0.025
		self.TF=timeFrame
		self.pairs=pairs
		self.establishPrice()
		bnStream(pairs, timeFrame,[self.Eye])


	def establishPrice(self):
		'''Establish the previous day's open to comile into dictionary upon startup
		To be used as a reference price for the price watch'''
		self.reference={}
		for pair in self.pairs:
			tik=ccxt.binance().fetch_ohlcv(symbol=pair, timeframe=self.TF, since=int(time.time()/86400)*86400*1000)
			tik=tik[0][4]
			self.reference.update({pair:tik})
		print(self.reference)


	def Eye(self, klines):
		market =languageHandler(output_lang = 'TradeModule',inputs =[klines.market],input_lang = "Binance")[0]
		price = klines.kClose
		print(f'{market}: {price}')
		if price > self.reference[market]*(1+self.movement):
			print(f'{market} {self.movement*100}% above reference price')
			self.reference.update({market:price})
			print(f'{market} reference price updated: {price}')

		elif price < self.reference[market]*(1-self.movement):
			#Send Bear Alert
			print(f'{market} {self.movement*100}% below reference price')
			self.reference.update({market:price})
			print(f'{market} reference price updated: {price}')

	def Hermes(self, msg):


pairlist=['BTC/USDT',
'ETH/USDT',
'NEO/USDT',
'MCO/BTC']

Eckleburg(pairlist, '1d')