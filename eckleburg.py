from bnWebsocket.klines import bnStream
from bnWebsocket.languageHandled import languageHandler
from slackclient import SlackClient
from bnWebsocket.keychain import slack  
import datetime
import ccxt
import time



class Eckleburg():
	def __init__(self, pairs, timeFrame):
		self.movement=0.00025
		self.TF=timeFrame
		self.pairs=pairs
		self.sc=SlackClient(slack.PriceAlertApp('BotUser'))
		self.sc_read=SlackClient(slack.PriceAlertApp('OAuth'))
		self.establishPrice()
		bnStream(pairs, timeFrame,[self.TetherAmend])


	def establishPrice(self):
		'''Establish the previous day's open to comile into dictionary upon startup
		To be used as a reference price for the price watch'''
		self.reference={}
		self.tetherOff=ccxt.binance().fetch_ohlcv(symbol='TUSD/USDT', timeframe=self.TF, since=int(time.time()/86400)*86400*1000)[0][4]
		for pair in self.pairs:
			tik=ccxt.binance().fetch_ohlcv(symbol=pair, timeframe=self.TF, since=int(time.time()/86400)*86400*1000)
			tik=tik[0][4]
			if pair[-4:] == 'USDT' and pair != 'TUSD/USDT':
				tik=tik/self.tetherOff
			self.reference.update({pair:tik})
		print(self.reference)

	def TetherAmend(self,klines):
		if klines.market == 'TUSDUSDT':
			self.tetherOff=klines.kClose
			priceA=klines.kClose
			market=klines.market
		elif klines.market[-4:] == 'USDT':
			priceA=klines.kClose/self.tetherOff
			market=klines.market[:-1]
		else:
			priceA=klines.kClose
			market=klines.market
		newDic={'market':market,'price':priceA}
		self.Eye(newDic,klines)



	def Eye(self, tik, klines):
		'''Last price vs. Reference Price'''
		market =languageHandler(output_lang = 'TradeModule',inputs =[klines.market],input_lang = "Binance")[0]
		printmarket=tik['market']
		price = tik['price']
		if printmarket[-3:]=='USD':
			print(f'{printmarket}: {price:.2f}')
		else:
			print(f'{printmarket}: {price:.8f}')

		if price > self.reference[market]*(1+self.movement):
			msg=f'{printmarket}: {self.movement*100}% above reference price [{price:.4f}]'
			print(msg)
			self.reference.update({market:price})
			print(f'{printmarket} reference price updated: {price}')
			self.Hermes(msg)

		elif price < self.reference[market]*(1-self.movement):
			msg=f'{printmarket}: {self.movement*100}% below reference price [{price:.4f}]'
			print(msg)
			self.reference.update({market:price})
			print(f'{printmarket} reference price updated: {price}')
			self.Hermes(msg)


	def Hermes(self, msg):
		'''Send Message on Slack'''
		try:
			self.sc.api_call('chat.postMessage', channel=slack.IDs('levelalert'), text=msg)	
		except:
			print(datetime.datetime.now(), 'ERROR: Message failed to send')





pairlist=['TUSD/USDT',
'BTC/USDT',
'ETH/USDT',
'ADA/USDT',
'XRP/USDT',
'NEO/USDT',
'MCO/BTC',
]

Eckleburg(pairlist, '1d')