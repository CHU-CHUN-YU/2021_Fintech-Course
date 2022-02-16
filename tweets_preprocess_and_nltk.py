import json
import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import requests
from pathlib import Path
import re
import urllib
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

os.makedirs(path+'filtertweets')
files=os.listdir(path+'tweets/tweets_timeline/')
for file in files:
  os.makedirs(path+'filtertweets/tweets_timeline/'+file)
for file in files:
  docs=os.listdir(path+'tweets/tweets_timeline/'+file)
  for doc in docs:
    data=pd.read_json(path+'tweets/tweets_timeline/'+file+'/'+doc)
    data=data[data['text'].str.contains('Bitcoin|bitcoin|Bitcoins|bitcoins|BitCoin|BitCoins|BTC|btc')]
    data=data.reset_index(drop=True)
    data.to_json(path+'filtertweets/tweets_timeline/'+file+'/'+doc)
os.makedirs(path+'filtettweets_clean')
files=os.listdir(path+'filtertweets/tweets_timeline/')
for file in files:
  os.makedirs(path+'filtertweets_clean/tweets_timeline/'+file)
# remove all the emojis 
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)
files=os.listdir(path+'filtertweets/tweets_timeline/')
for file in files:
  docs=os.listdir(path+'filtertweets/tweets_timeline/'+file)
 
  for doc in docs:
    data=pd.read_json(path+'filtertweets/tweets_timeline/'+file+'/'+doc)
    data['text']=data['text'].apply(deEmojify) #remove all the emojis 
    data['text_cleanV1']=''
     
    for i in range(data.shape[0]):
        tweet=data['text'][i]
        tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","",tweet) #Remove @ sign
        tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
        data['text_cleanV1'][i]=tweet.replace("#", "").replace("_", " ").replace("\n", " ") #Remove hashtag sign but keep the text
  
    data.to_json(path+'filtertweets_clean/tweets_timeline/'+file+'/'+doc)
# 刪除 空白的 json
files=os.listdir(path+'filtertweets_clean/tweets_timeline/')
for file in files:
  docs=os.listdir(path+'filtertweets_clean/tweets_timeline/'+file)
  for doc in docs:
    data=pd.read_json(path+'filtertweets_clean/tweets_timeline/'+file+'/'+doc)
    if(data.shape[0]==0):
      print(path+'filtertweets_clean/tweets_timeline/'+file+'/'+doc)
      os.remove(path+'filtertweets_clean/tweets_timeline/'+file+'/'+doc)
# 刪除 空白的 id 資料夾
files=os.listdir(path+'filtertweets_clean/tweets_timeline/')
for file in files:
  docs=os.listdir(path+'filtertweets_clean/tweets_timeline/'+file)
  if (len(docs)==0):
    print(path+'filtertweets_clean/tweets_timeline/'+file)
    os.rmdir(path+'filtertweets_clean/tweets_timeline/'+file)  
#candles data
#4h candles
files_4h=os.listdir(path+'candles/btcusdt/14400/')
price_df_4h=pd.DataFrame()
for file in files_4h:
  json_4h=open(path + 'candles/btcusdt/14400/'+file)
  price_4h = json.load(json_4h)
  data_4h=pd.DataFrame(price_4h['14400'],columns=['CloseTime','OpenPrice','HighPrice','LowPrice','ClosePrice','Volume','QuoteVolume'])
  price_df_4h=pd.concat([price_df_4h,data_4h], ignore_index=True)
#6h candles
files_6h=os.listdir(path+'candles/btcusdt/21600/')
price_df_6h=pd.DataFrame()
for file in files_6h:
  json_6h=open(path + 'candles/btcusdt/21600/'+file)
  price_6h = json.load(json_6h)
  data_6h=pd.DataFrame(price_6h['21600'],columns=['CloseTime','OpenPrice','HighPrice','LowPrice','ClosePrice','Volume','QuoteVolume'])
  price_df_6h=pd.concat([price_df_6h,data_6h], ignore_index=True)
#12h candles
files_12h=os.listdir(path+'candles/btcusdt/43200/')
price_df_12h=pd.DataFrame()
for file in files_12h:
  json_12h=open(path + 'candles/btcusdt/43200/'+file)
  price_12h = json.load(json_12h)
  data_12h=pd.DataFrame(price_12h['43200'],columns=['CloseTime','OpenPrice','HighPrice','LowPrice','ClosePrice','Volume','QuoteVolume'])
  price_df_12h=pd.concat([price_df_12h,data_12h], ignore_index=True)
price_df_4h=price_df_4h.drop_duplicates()
price_df_6h=price_df_6h.drop_duplicates()
price_df_12h=price_df_12h.drop_duplicates()
price_df_4h=price_df_4h.reset_index(drop=True)
price_df_6h=price_df_6h.reset_index(drop=True)
price_df_12h=price_df_12h.reset_index(drop=True)
#Change Rate of ClosePrice
price_df_4h['Close_change']=0
price_df_4h['Close_change'][1:len(price_df_4h)]=[(price_df_4h['ClosePrice'][i]-price_df_4h['ClosePrice'][i-1])*100/price_df_4h['ClosePrice'][i-1] for i in range(1,len(price_df_4h))]
price_df_6h['Close_change']=0
price_df_6h['Close_change'][1:len(price_df_6h)]=[(price_df_6h['ClosePrice'][i]-price_df_6h['ClosePrice'][i-1])*100/price_df_6h['ClosePrice'][i-1] for i in range(1,len(price_df_6h))]
price_df_12h['Close_change']=0
price_df_12h['Close_change'][1:len(price_df_12h)]=[(price_df_12h['ClosePrice'][i]-price_df_12h['ClosePrice'][i-1])*100/price_df_12h['ClosePrice'][i-1] for i in range(1,len(price_df_12h))]

#tweets 
tweets=pd.DataFrame()
tweetspath=os.listdir(path+'filtertweets_clean/tweets_timeline/')
for ids in tweetspath:
  filepath=os.listdir(path+'filtertweets_clean/tweets_timeline/'+ids+'/')
  for file in filepath:
    json_tweets=open(path+'filtertweets_clean/tweets_timeline/'+ids+'/'+file)
    tweets_df=pd.read_json(json_tweets)
    tweets=pd.concat([tweets,tweets_df],ignore_index=True)
tweets=tweets.drop(['text'],axis=1)
tweets=tweets.sort_values(by=['created_at'])
tweets=tweets.reset_index(drop=True)
tweets['like_count']=pd.Series(tweets['public_metrics'][i]['like_count']for i in range(len(tweets)))
tweets['quote_count']=pd.Series(tweets['public_metrics'][i]['quote_count']for i in range(len(tweets)))
tweets['reply_count']=pd.Series(tweets['public_metrics'][i]['reply_count']for i in range(len(tweets)))
tweets['retweet_count']=pd.Series(tweets['public_metrics'][i]['retweet_count']for i in range(len(tweets)))
tweets=tweets.drop(['public_metrics'],axis=1)
sia = SIA()
tweets['pos']=pd.Series()
tweets['neu']=pd.Series()
tweets['neg']=pd.Series()
tweets['sent_score']=pd.Series()
tweets['sent']=pd.Series()
for idx in range(len(tweets)):
  tweets['pos'][idx]=sia.polarity_scores(tweets['text_cleanV1'][idx])['pos']
  tweets['neu'][idx]=sia.polarity_scores(tweets['text_cleanV1'][idx])['neu']
  tweets['neg'][idx]=sia.polarity_scores(tweets['text_cleanV1'][idx])['neg']
  tweets['sent_score'][idx]=sia.polarity_scores(tweets['text_cleanV1'][idx])['compound']
for i in range(len(tweets)):
  if tweets['sent_score'][i]==0:
    tweets['sent'][i]='neu'
  if tweets['sent_score'][i]>0:
    tweets['sent'][i]='pos'
  if tweets['sent_score'][i]<0:
    tweets['sent'][i]='neg'
tweets_v1=tweets[abs(tweets_raw['sent'])>0.0]
tweets=tweets_v1.reset_index(drop=True)
tweets['pos_neg']=pd.Series()
for i in range(len(tweets)):
  if tweets['sent'][i]>0:
    tweets['pos_neg'][i]='pos'
  else:tweets['pos_neg'][i]='neg'

#slice tweets by time period and merge tweets
tweets_4h=pd.DataFrame(columns=['time','text','change','top_like','avg_like','top_quote','avg_quote','top_reply','avg_reply','top_RT','avg_RT','pos_count','neg_count'])
tweets_6h=pd.DataFrame(columns=['time','text','change','top_like','avg_like','top_quote','avg_quote','top_reply','avg_reply','top_RT','avg_RT','pos_count','neg_count'])
tweets_12h=pd.DataFrame(columns=['time','text','change','top_like','avg_like','top_quote','avg_quote','top_reply','avg_reply','top_RT','avg_RT','pos_count','neg_count'])
start_timestamp=1609459200
now_timestamp_4h=start_timestamp+14400
now_timestamp=start_timestamp+21600
now_timestamp_12h=start_timestamp+43200
text_4h=''
count_4h=0
like_4h=0
reply_4h=0
quote_4h=0
RT_4h=0
pos_4h=0
neg_4h=0
likes_4h=[0]
replys_4h=[0]
quotes_4h=[0]
RTs_4h=[0]
text_6h=''
count_6h=0
like_6h=0
reply_6h=0
quote_6h=0
RT_6h=0
pos_6h=0
neg_6h=0
likes_6h=[0]
replys_6h=[0]
quotes_6h=[0]
RTs_6h=[0]
text_12h=''
count_12h=0
like_12h=0
reply_12h=0
quote_12h=0
RT_12h=0
pos_12h=0
neg_12h=0
likes_12h=[0]
replys_12h=[0]
quotes_12h=[0]
RTs_12h=[0]
#slice 4 hour
for i in range(len(tweets)):
  timestamp=tweets['created_at'][i]
  if timestamp<datetime.fromtimestamp(now_timestamp_4h):
    if tweets['pos_neg'][i]=='pos':
      pos_4h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_4h+=1
    text_4h=text_4h+tweets['text_cleanV1'][i]
    count_4h+=1
    like_4h+=tweets['like_count'][i]
    reply_4h+=tweets['reply_count'][i]
    quote_4h+=tweets['quote_count'][i]
    RT_4h+=tweets['retweet_count'][i]
    likes_4h.append(tweets['like_count'][i])
    replys_4h.append(tweets['reply_count'][i])
    quotes_4h.append(tweets['quote_count'][i])
    RTs_4h.append(tweets['retweet_count'][i])
  if timestamp>datetime.fromtimestamp(now_timestamp_4h):
    if count_4h!=0:
      like_4h/=count_4h
      reply_4h/=count_4h
      quote_4h/=count_4h
      RT_4h/=count_4h
    else:
      like_4h=0
      reply_4h=0
      quote_4h=0
      RT_4h=0
    tweets_4h=tweets_4h.append({'time':datetime.fromtimestamp(now_timestamp_4h),'text':text_4h,'top_like':max(likes_4h),'avg_like':like_4h,'top_reply':max(replys_4h),'avg_reply':reply_4h,'top_quote':max(quotes_4h),'avg_quote':quote_4h,'top_RT':max(RTs_4h),'avg_RT':RT_4h,'pos_count':pos_4h,'neg_count':neg_4h},ignore_index=True)
    now_timestamp_4h+=14400
    text_4h=''
    like_4h=0
    reply_4h=0
    quote_4h=0
    RT_4h=0
    count_4h=0
    pos_4h=0
    neg_4h=0
    likes_4h=[0]
    replys_4h=[0]
    quotes_4h=[0]
    RTs_4h=[0]
    if tweets['pos_neg'][i]=='pos':
      pos_4h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_4h+=1
    like_4h+=tweets['like_count'][i]
    reply_4h+=tweets['reply_count'][i]
    quote_4h+=tweets['quote_count'][i]
    RT_4h+=tweets['retweet_count'][i]
    text_4h=text_6h+tweets['text_cleanV1'][i]
    likes_4h.append(tweets['like_count'][i])
    replys_4h.append(tweets['reply_count'][i])
    quotes_4h.append(tweets['quote_count'][i])
    RTs_4h.append(tweets['retweet_count'][i])
    count_4h+=1
tweets_4h=tweets_4h.append({'time':datetime.fromtimestamp(now_timestamp_4h),'text':text_4h,'top_like':max(likes_4h),'avg_like':like_4h,'top_reply':max(replys_4h),'avg_reply':reply_4h,'top_quote':max(quotes_6h),'avg_quote':quote_4h,'top_RT':max(RTs_4h),'avg_RT':RT_4h,'pos_count':pos_4h,'neg_count':neg_4h},ignore_index=True)
#slice 6 hour
for i in range(len(tweets)):
  timestamp=tweets['created_at'][i]
  if timestamp<datetime.fromtimestamp(now_timestamp):
    if tweets['pos_neg'][i]=='pos':
      pos_6h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_6h+=1
    text_6h=text_6h+tweets['text_cleanV1'][i]
    count_6h+=1
    like_6h+=tweets['like_count'][i]
    reply_6h+=tweets['reply_count'][i]
    quote_6h+=tweets['quote_count'][i]
    RT_6h+=tweets['retweet_count'][i]
    likes_6h.append(tweets['like_count'][i])
    replys_6h.append(tweets['reply_count'][i])
    quotes_6h.append(tweets['quote_count'][i])
    RTs_6h.append(tweets['retweet_count'][i])
  if timestamp>datetime.fromtimestamp(now_timestamp):
    if count_6h!=0:
      like_6h/=count_6h
      reply_6h/=count_6h
      quote_6h/=count_6h
      RT_6h/=count_6h
    else:
      like_6h=0
      reply_6h=0
      quote_6h=0
      RT_6h=0
    tweets_6h=tweets_6h.append({'time':datetime.fromtimestamp(now_timestamp),'text':text_6h,'top_like':max(likes_6h),'avg_like':like_6h,'top_reply':max(replys_6h),'avg_reply':reply_6h,'top_quote':max(quotes_6h),'avg_quote':quote_6h,'top_RT':max(RTs_6h),'avg_RT':RT_6h,'pos_count':pos_6h,'neg_count':neg_6h},ignore_index=True)
    now_timestamp+=21600
    text_6h=''
    like_6h=0
    reply_6h=0
    quote_6h=0
    RT_6h=0
    count_6h=0
    pos_6h=0
    neg_6h=0
    likes_6h=[0]
    replys_6h=[0]
    quotes_6h=[0]
    RTs_6h=[0]
    if tweets['pos_neg'][i]=='pos':
      pos_6h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_6h+=1
    like_6h+=tweets['like_count'][i]
    reply_6h+=tweets['reply_count'][i]
    quote_6h+=tweets['quote_count'][i]
    RT_6h+=tweets['retweet_count'][i]
    text_6h=text_6h+tweets['text_cleanV1'][i]
    likes_6h.append(tweets['like_count'][i])
    replys_6h.append(tweets['reply_count'][i])
    quotes_6h.append(tweets['quote_count'][i])
    RTs_6h.append(tweets['retweet_count'][i])
    count_6h+=1
tweets_6h=tweets_6h.append({'time':datetime.fromtimestamp(now_timestamp),'text':text_6h,'top_like':max(likes_6h),'avg_like':like_6h,'top_reply':max(replys_6h),'avg_reply':reply_6h,'top_quote':max(quotes_6h),'avg_quote':quote_6h,'top_RT':max(RTs_6h),'avg_RT':RT_6h,'pos_count':pos_6h,'neg_count':neg_6h},ignore_index=True)
#slice 12 hour
for i in range(len(tweets)):
  timestamp=tweets['created_at'][i]
  if timestamp<datetime.fromtimestamp(now_timestamp_12h):
    if tweets['pos_neg'][i]=='pos':
      pos_12h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_12h+=1
    text_12h=text_12h+tweets['text_cleanV1'][i]
    count_12h+=1
    like_12h+=tweets['like_count'][i]
    reply_12h+=tweets['reply_count'][i]
    quote_12h+=tweets['quote_count'][i]
    RT_12h+=tweets['retweet_count'][i]
    likes_12h.append(tweets['like_count'][i])
    replys_12h.append(tweets['reply_count'][i])
    quotes_12h.append(tweets['quote_count'][i])
    RTs_12h.append(tweets['retweet_count'][i])
  if timestamp>datetime.fromtimestamp(now_timestamp_12h):
    if count_12h!=0:
      like_12h/=count_12h
      reply_12h/=count_12h
      quote_12h/=count_12h
      RT_12h/=count_12h
    else:
      like_12h=0
      reply_12h=0
      quote_12h=0
      RT_12h=0
    tweets_12h=tweets_12h.append({'time':datetime.fromtimestamp(now_timestamp_12h),'text':text_12h,'top_like':max(likes_12h),'avg_like':like_12h,'top_reply':max(replys_12h),'avg_reply':reply_12h,'top_quote':max(quotes_12h),'avg_quote':quote_12h,'top_RT':max(RTs_12h),'avg_RT':RT_12h,'pos_count':pos_12h,'neg_count':neg_12h},ignore_index=True)
    now_timestamp_12h+=43200
    text_12h=''
    count_12h=0
    like_12h=0
    reply_12h=0
    quote_12h=0
    RT_12h=0
    pos_12h=0
    neg_12h=0
    likes_12h=[0]
    replys_12h=[0]
    quotes_12h=[0]
    RTs_12h=[0]
    if tweets['pos_neg'][i]=='pos':
      pos_12h+=1
    if tweets['pos_neg'][i]=='neg':
      neg_12h+=1
    text_12h=text_12h+tweets['text_cleanV1'][i]
    like_12h+=tweets['like_count'][i]
    reply_12h+=tweets['reply_count'][i]
    quote_12h+=tweets['quote_count'][i]
    RT_12h+=tweets['retweet_count'][i]
    likes_12h.append(tweets['like_count'][i])
    replys_12h.append(tweets['reply_count'][i])
    quotes_12h.append(tweets['quote_count'][i])
    RTs_12h.append(tweets['retweet_count'][i])
    count_12h+=1
tweets_12h=tweets_12h.append({'time':datetime.fromtimestamp(now_timestamp_12h),'text':text_12h,'top_like':max(likes_12h),'avg_like':like_12h,'top_reply':max(replys_12h),'avg_reply':reply_12h,'top_quote':max(quotes_12h),'avg_quote':quote_12h,'top_RT':max(RTs_12h),'avg_RT':RT_12h,'pos_count':pos_12h,'neg_count':neg_12h},ignore_index=True)
sia = SIA()
tweets_4h['sent']=pd.Series()
tweets_6h['sent']=pd.Series()
tweets_12h['sent']=pd.Series()
for idx_4h in range(len(tweets_4h)):
  tweets_4h['sent'][idx_4h]=sia.polarity_scores(tweets_4h['text'][idx_4h])['compound']
for idx_6h in range(len(tweets_6h)):
  tweets_6h['sent'][idx_6h]=sia.polarity_scores(tweets_6h['text'][idx_6h])['compound']
for idx_12h in range(len(tweets_12h)):
  tweets_12h['sent'][idx_12h]=sia.polarity_scores(tweets_12h['text'][idx_12h])['compound']
#change
tweets_4h['change'][:]=price_df_4h['Close_change'][1:]
tweets_6h['change'][:]=price_df_6h['Close_change'][1:]
tweets_12h['change'][:]=price_df_12h['Close_change'][1:]
#up/down
tweets_4h['up_down']=[1 if price_df_4h['Close_change'][i]>0 else 0 for i in range(1,len(price_df_4h))]
tweets_6h['up_down']=[1 if price_df_6h['Close_change'][i]>0 else 0 for i in range(1,len(price_df_6h))]
tweets_12h['up_down']=[1 if price_df_12h['Close_change'][i]>0 else 0 for i in range(1,len(price_df_12h))]

#save data
tweets_4h.to_csv(path+'/tweets_with_price/tweets_4h_sen_count.csv')
tweets_6h.to_csv(path+'/tweets_with_price/tweets_6h_sen_count.csv')
tweets_12h.to_csv(path+'/tweets_with_price/tweets_12h_sen_count.csv')