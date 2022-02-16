import json
import tensorflow as tf
import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import requests
from requests_oauthlib import OAuth1
from pathlib import Path
import re
import urllib

!pip install cryptowatch-sdk
import cryptowatch as cw

cw.api_key = "" #your cryptowatch auth keys here
twauth = OAuth1('', '', '', '') #your twitter auth keys here

def time_twitter_to_dt(str):
  return datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')
def time_unix_to_dt(int):
  return datetime.fromtimestamp(int)
def time_dt_to_unix(dtObj):
  return int(dtObj.timestamp())
def time_twitter_to_unix(str):
  return int(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
def create_twitter_time(Y, M, D, h = 0, m = 0, s = 0):
  return str(Y).zfill(4) + '-' + str(M).zfill(2) + '-' + str(D).zfill(2) + 'T' + str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2) + 'Z'
def create_unix_time(Y, M, D, h = 0, m = 0, s = 0):
  return int(datetime(Y, M, D, h, m, s).timestamp())

def encode_str_url(string):
  return urllib.parse.quote_plus(string)

def retrieve_tweets_timeline(id, start_time, end_time, name):
  link = 'https://api.twitter.com/2/users/' + id + '/tweets?tweet.fields=id,created_at,public_metrics&max_results=100' + '&start_time=' + start_time + '&end_time=' + end_time
  tweet = requests.get(link, auth=twauth)
  tweets = json.loads(tweet.text)
  if 'data' in tweets:
    tweets = tweets['data']
    print('Success' + name)
    tar = path + 'tweets/tweets_timeline/' + id + '/'
    if not os.path.exists(tar):
       os.makedirs(tar)
    with open(tar + name + '.json', 'w') as outfile:
      json.dump(tweets,outfile)
  else:
    print('Bad Request' + name)
    #with open(path + 'tweets/tweets_timeline/' + name +'.json', 'w') as outfile:
      #json.dump(tweets,outfile)

personal = {'elonmusk': '44196397', 'jack': '12' , 'justinsuntron': '902839045356744704', 'rogerkver': '176758255', 'aantonop': '1469101279', 'ErikVoorhees': '61417559', 'bgarlinghouse': '28582680', 'BarrySilbert': '396045469', 'VitalikButerin': '295218901', 'cz_binance': '902926941413453824', 'justinsuntron': '902839045356744704', 'GordoCryptos': '935542316323835905', 'saylor': '244647486', 'IOHK_Charles': '1376161898', 'TaylorMusk_': '227233892', 'elliotrades': '948736680554409984', 'APompliano': '339061487', 'SBF_FTX': '1110877798820777986'}
news = {'CoinDesk': '1333467482', 'Cointelegraph': '2207129125', 'todayonchain': '981416882875125762', 'newsbtc': '2150123534', 'BitcoinMagazine': '361289499', 'CryptoSlate': '893284234042855424', 'bitcoinist': '2338070737', 'nulltxnews': '2509810398', 'BitcoinCom': '380069391', 'CryptovestMedia': '913315593750683648', 'iiblockchain': '912906507431432193', 'blockonomi': '34351198', 'coinspeaker': '2379303330', 'CoinMarketCap': '2260491445', 'whale_alert': '1039833297751302144'}
exchange = {'binance': '877807935493033984', 'FTX_Official': '1101264495337365504', 'coinbase': '574032254', 'krakenfx': '1399148563', 'kucoincom': '910110294625492992', 'HuobiGlobal': '914029581610377217', 'cryptocom': '864347902029709314'}

def retrieve(user_ids):
  for id in user_ids:
      counter = 0
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 1, 1)), encode_str_url(create_twitter_time(2021, 1, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 1, 16)), encode_str_url(create_twitter_time(2021, 1, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 2, 1)), encode_str_url(create_twitter_time(2021, 2, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 2, 16)), encode_str_url(create_twitter_time(2021, 2, 28)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 3, 1)), encode_str_url(create_twitter_time(2021, 3, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 3, 16)), encode_str_url(create_twitter_time(2021, 3, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 4, 1)), encode_str_url(create_twitter_time(2021, 4, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 4, 16)), encode_str_url(create_twitter_time(2021, 4, 30)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 5, 1)), encode_str_url(create_twitter_time(2021, 5, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 5, 16)), encode_str_url(create_twitter_time(2021, 5, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 6, 1)), encode_str_url(create_twitter_time(2021, 6, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 6, 16)), encode_str_url(create_twitter_time(2021, 6, 30)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 7, 1)), encode_str_url(create_twitter_time(2021, 7, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 7, 16)), encode_str_url(create_twitter_time(2021, 7, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 8, 1)), encode_str_url(create_twitter_time(2021, 8, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 8, 16)), encode_str_url(create_twitter_time(2021, 8, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 9, 1)), encode_str_url(create_twitter_time(2021, 9, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 9, 16)), encode_str_url(create_twitter_time(2021, 9, 30)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 10, 1)), encode_str_url(create_twitter_time(2021, 10, 15)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 10, 16)), encode_str_url(create_twitter_time(2021, 10, 31)), str(counter).zfill(3))
      counter += 1
      retrieve_tweets_timeline(user_ids[id], encode_str_url(create_twitter_time(2021, 11, 1)), encode_str_url(create_twitter_time(2021, 11, 11)), str(counter).zfill(3))
      counter += 1


retrieve(personal)
retrieve(news)
retrieve(exchange)

def get_candles(pair, after, before, period, name):
  url = 'https://api.cryptowat.ch/markets/binance/' + pair + '/ohlc'
  candles = requests.get(url, params = {'after': after, 'before': before,'periods': [period], 'apikey': cw.api_key})
  candles = json.loads(candles.text)
  if 'result' in candles:
    candles = candles['result']
    print('Success')
    with open(path + 'candles/' + pair + '/' + str(period) + '/' + name + '.json', 'w') as cryptojson:
      json.dump(candles, cryptojson)
  else:
    print('Bad Request')
    print(candles)


coinpairs = ['btcusdt', 'ethusdt', 'solusdt', 'shibusdt']
periods = [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400]

for pair in coinpairs:
  for period in periods:
    get_candles(pair, create_unix_time(2021, 1, 1), create_unix_time(2021, 2, 1), period, '0')
    get_candles(pair, create_unix_time(2021, 2, 1), create_unix_time(2021, 3, 1), period, '1')
    get_candles(pair, create_unix_time(2021, 3, 1), create_unix_time(2021, 4, 1), period, '2')
    get_candles(pair, create_unix_time(2021, 4, 1), create_unix_time(2021, 5, 1), period, '3')
    get_candles(pair, create_unix_time(2021, 5, 1), create_unix_time(2021, 6, 1), period, '4')
    get_candles(pair, create_unix_time(2021, 6, 1), create_unix_time(2021, 7, 1), period, '5')
    get_candles(pair, create_unix_time(2021, 7, 1), create_unix_time(2021, 8, 1), period, '6')
    get_candles(pair, create_unix_time(2021, 8, 1), create_unix_time(2021, 9, 1), period, '7')
    get_candles(pair, create_unix_time(2021, 9, 1), create_unix_time(2021, 10, 1), period, '8')
    get_candles(pair, create_unix_time(2021, 10, 1), create_unix_time(2021, 11, 1), period, '9')
    get_candles(pair, create_unix_time(2021, 11, 1), create_unix_time(2021, 11, 11), period, '10')

