from bnWebsocket.klines import bnStream
import ccxt
import time




class Eckleburg():
	def __init__(self, pairs, timeFrame):
		self.TF=timeFrame
		self.pairs=pairs
		self.establishTime()
		self.establishPrice()
		bnStream(pairs, timeFrame,[self.TimeMangement])

	def establishTime(self):
		print('GMT-0 Established')
		self.gmt0=int(time.time()/86400)

	def establishPrice(self):
		for pair in self.pairs:
			tik=ccxt.binance().fetch_ohlcv(symbol=pair, timeframe=self.TF, since=(int(time.time()/86400)*86400-86401)*1000)
			print(pair, tik)

	def TimeMangement(self, klines):
		if time.time()-self.gmt0*86400<(86400/2):
			print(time.time()-self.gmt0*86400)
			print('nothing')
		else:
			self.establishTime()


	def Printer(self, klines):
		print(klines)




Eckleburg(['BTC/USDT'], '1d')