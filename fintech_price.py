# -*- coding: utf-8 -*-
"""Fintech_price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QBhZROdwHbFW0IbxubSTILDSuMwpIUjQ

# 1. Download and import packages
"""

!pip3 install mpl_finance
!pip3 install talib-binary

import json
# import xarray as xr
import pandas as pd
import numpy as np
import random

from datetime import datetime
import mpl_finance as mpf
import talib
import matplotlib.pyplot as plt

from keras import Sequential
from keras import models
from keras import layers
from keras.callbacks import EarlyStopping 
from tensorflow.keras.optimizers import Adam

"""# 2. Data import"""

from google.colab import drive
drive.mount('/content/drive')

loc = 'drive/My Drive/'
all_df = {}
# period_selection = [7200, 14400, 21600, 43200, 86400]
# use 4 hours for example
period_selection = [14400]
for i in period_selection:
  store = []
  for j in range(0,11):
      f = open(loc+ str(i) +'/' + str(j) +'.json')
      dic = json.load(f)
      
      tmp = dic[str(i)]
      store = store + tmp
      
  all_df[i] = pd.DataFrame(store)
  all_df[i].columns = ['CloseTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'QuoteVolume']
  all_df[i]['CloseTime'] =[datetime.fromtimestamp(ele) for ele in all_df[i]['CloseTime']]

"""# 3. Time period selection"""

time_period = 14400
tmp= technical_index(all_df[time_period])

"""# 4. Variable selection
# 5. Data split
# 6. Min-Max transformation
"""

# lag
lag_period = [3, 6, 9, 12]

# define function for adding technical_index, data split and min_max transformation
def technical_index(input_df):#, lag):
  df = input_df
  
  # 1. moving average
  df['MA5'] = talib.SMA(np.array(df['Close']), 5)
  df['MA10'] = talib.SMA(np.array(df['Close']), 10)
  df['MA20'] = talib.SMA(np.array(df['Close']), 20)

  # 2. KD
  df['K'], df['D'] = talib.STOCH(df['High'], df['Low'], df['Close'])

  # 3. MACD
  df['MACD'], df['MACD_S'], df['MACD_H'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

  # 4. RSI
  df['RSI'] = talib.RSI(df['Close'], timeperiod=14) / talib.RSI(df['Close'], timeperiod=14).mean()

  # 5. ADX
  df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14) / \
                  talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14).mean()
  df['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=14) / \
                  talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=14).mean()

  # 6. Bollinger 
  df['BBANDS_U'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[0] / \
                    talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[0].mean()
  df['BBANDS_M'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1] / \
                    talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1].mean()
  df['BBANDS_L'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2] / \
                    talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2].mean()
  
  return df

def z_scale(x_org):
  if len(x_org.shape) > 1:
      x = x_org.drop('CloseTime', axis=1)
  else:
      x = x_org
  
  z = (x - x.min()) / (x.max() - x.min())
  min_info = x.min()
  max_info = x.max()
  if len(x_org.shape) > 1:
      df_info = pd.DataFrame({'min': min_info, 'max': max_info})
  else:
      df_info = [min_info, max_info]    
      
  return z, df_info

def generate_data(dat, col_name):
  y = dat['Close']
  total_dat = dat.drop(col_name, axis=1)
  test_x, test_info = z_scale(total_dat.loc[total_dat['CloseTime'] >= datetime(2021, 10, 1),])
  valid_x, valid_info = z_scale(total_dat.loc[(total_dat['CloseTime'] < datetime(2021, 10, 1)) & \
                                                (total_dat['CloseTime'] >= datetime(2021, 8, 1)),])
  train_x, train_info = z_scale(total_dat.loc[total_dat['CloseTime'] < datetime(2021, 8, 1),])
  test_y, test_y_info = z_scale(y[total_dat['CloseTime'] >= datetime(2021, 10, 1)])
  valid_y, valid_y_info = z_scale(y[(total_dat['CloseTime'] < datetime(2021, 10, 1)) & \
                                    (total_dat['CloseTime'] >= datetime(2021, 8, 1))])
  train_y, train_y_info = z_scale(y[total_dat['CloseTime'] < datetime(2021, 8, 1)])
  
  return train_x, train_y, valid_x, valid_y, test_x, test_y, train_y_info, valid_y_info, test_y_info

"""# 7. Hypertune for each model combination

### Without Tweet (Only Price, volume and technical indicator are included)
"""

# without twitter
for lag_cnt in lag_period:
  dat = tmp.dropna(axis=0)

  col_name = list(dat.columns)
  col_name.remove('CloseTime')
  for i in col_name:
    for j in range(1,lag_cnt+1):
        dat[i+'_lag'+str(j)] = dat[i].shift(j)
          
  dat = dat.dropna(axis=0)

  train_x, train_y, valid_x, valid_y, test_x, \
    test_y, train_y_info, valid_y_info, test_y_info = generate_data(dat, col_name)
  # import tensorflow as tf
  # device_name = tf.test.gpu_device_name()
  # with tf.device('/device:GPU:0'):
  node_cnt1 = [32, 64, 128, 256]
  node_cnt2 = [32, 64, 128, 256]
  lr = [0.001]
  callback = EarlyStopping(monitor='loss', patience=5)

  para_dict = {'dense_node': node_cnt2,
          'lr': lr,
          'epochs':[100],
          'batch_size':[32, 64, 128],
          'dropout_rate':[0.1,0.2,0.4,0.6]}

  for layer_cnt in [2]:
    for k in range(layer_cnt): 
        para_dict['node'+str(k+1)] = eval('node_cnt'+str(k+1))

    loss_dict = {}
    val_loss_dict = {}
    info = {}
    iter_cnt = 0
    for k in para_dict['dropout_rate']:
      for i in node_cnt1:
        for n2 in node_cnt2:
          for j in para_dict['batch_size']:
            random.seed(iter_cnt+1)
            es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
            model = models.Sequential()
            model.add(layers.LSTM(i,input_shape=(train_x.shape[1], 1),
                                  kernel_regularizer='l2',return_sequences=True))
            model.add(layers.Dropout(k))
            model.add(layers.LSTM(i))
            model.add(layers.Dropout(k))
            model.add(layers.Dense(n2))
            model.add(layers.Dense(1))
            model.summary()

            model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
            history = model.fit(np.expand_dims(train_x, axis=2), train_y, 
                                epochs=100, 
                                batch_size=j, 
                                verbose=2,
                                callbacks = [es],
                                validation_data=(np.expand_dims(valid_x, axis=2), valid_y))
            history_dict = history.history


            # loss & accuracy
            info[iter_cnt] = 'node1='+str(i)+' node2='+str(n2)+' batch='+str(j)+' dropout='+str(k)
            loss_dict[iter_cnt] = history_dict['loss'][len(history_dict['loss'])-1]
            val_loss_dict[iter_cnt] = history_dict['val_loss'][len(history_dict['val_loss'])-1]
            print(info[iter_cnt]+' lag='+str(lag_cnt))
            if iter_cnt % 5 == 4:
              save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
              # save and download the result
              with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'.json', 'w', encoding='utf-8') as f:
                json.dump(save_dic, f, ensure_ascii=False)

            iter_cnt = iter_cnt + 1

  save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
  # save and download the result
  with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'.json', 'w', encoding='utf-8') as f:
    json.dump(save_dic, f, ensure_ascii=False)

save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
# save and download the result
dump_file = json.dumps ('save_dic')
encode_file = dump_file.encode('utf-8')
with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'.json', 'w') as f:
  f.write(str(encode_file))

"""### PCA """

# pca try
from sklearn.decomposition import PCA

pca_cnt = [10, 20, 30, 40]
lag_cnt = [9, 12]
for lag_cnt in lag_period:
  dat = tmp.dropna(axis=0)

  # add lag term
  col_name = list(dat.columns)
  col_name.remove('CloseTime')
  for i in col_name:
    for j in range(1,lag_cnt+1):
        dat[i+'_lag'+str(j)] = dat[i].shift(j)
          
  dat = dat.dropna(axis=0)
  
  for com_cnt in pca_cnt:
    train_x, train_y, valid_x, valid_y, test_x, \
      test_y, train_y_info, valid_y_info, test_y_info = generate_data(dat, col_name)
    
    # pca
    random.seed(com_cnt * 100)
    pca = PCA(n_components=com_cnt)
    train_x = pca.fit_transform(train_x)
    valid_x = pca.transform(valid_x)


    node_cnt1 = [32, 64, 128, 256]
    node_cnt2 = [32, 64, 128, 256]
    lr = [0.001]
    callback = EarlyStopping(monitor='loss', patience=5)

    para_dict = {'dense_node': node_cnt2,
            'lr': lr,
            'epochs':[100],
            'batch_size':[32, 64, 128],
            'dropout_rate':[0.1,0.2,0.4,0.6]}

    for layer_cnt in [2]:
      for k in range(layer_cnt): 
          para_dict['node'+str(k+1)] = eval('node_cnt'+str(k+1))

      loss_dict = {}
      val_loss_dict = {}
      info = {}
      iter_cnt = 0
      for k in para_dict['dropout_rate']:
        for i in node_cnt1:
          for n2 in node_cnt2:
            for j in para_dict['batch_size']:
              random.seed(iter_cnt+1)
              es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
              model = models.Sequential()
              model.add(layers.LSTM(i,input_shape=(train_x.shape[1], 1),
                                    kernel_regularizer='l2',return_sequences=True))
              model.add(layers.Dropout(k))
              model.add(layers.LSTM(i))
              model.add(layers.Dropout(k))
              model.add(layers.Dense(n2))
              model.add(layers.Dense(1))
              model.summary()

              model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
              history = model.fit(np.expand_dims(train_x, axis=2), train_y, 
                                  epochs=100, 
                                  batch_size=j, 
                                  verbose=2,
                                  callbacks = [es],
                                  validation_data=(np.expand_dims(valid_x, axis=2), valid_y))
              history_dict = history.history


              # loss & accuracy
              info[iter_cnt] = 'node1='+str(i)+' node2='+str(n2)+' batch='+str(j)+' dropout='+str(k)+' pca_cnt='+str(com_cnt)
              loss_dict[iter_cnt] = history_dict['loss'][len(history_dict['loss'])-1]
              val_loss_dict[iter_cnt] = history_dict['val_loss'][len(history_dict['val_loss'])-1]
              print(info[iter_cnt]+' lag='+str(lag_cnt))
              if iter_cnt % 5 == 4:
                save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
                # save and download the result
                with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'_pca'+str(com_cnt)+'.json', 'w', encoding='utf-8') as f:
                  json.dump(save_dic, f, ensure_ascii=False)

              iter_cnt = iter_cnt + 1

    save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
    # save and download the result
    with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'_pca'+str(com_cnt)+'.json', 'w', encoding='utf-8') as f:
      json.dump(save_dic, f, ensure_ascii=False)

"""### With Tweet"""

tweet = pd.read_csv('drive/Shareddrives/FinTech21/tweets_4h_with_sentscore_and_bertprediction.csv')
tweet = tweet.drop(list(tweet.columns)[0:1], axis=1)
tweet = tweet.drop(['text', 'change', 'up_down', 'label'], axis=1)
iter_col = list(tweet.columns)
iter_col.remove('time')
for i in iter_col:
  tweet[i] = tweet[i].shift(1)
tweet['time'] = pd.to_datetime(tweet['time'])
tweet.rename(columns={'time':'CloseTime'}, inplace=True)

# with twitter data
for lag_cnt in lag_period:
  dat = tmp.dropna(axis=0)

  col_name = list(dat.columns)
  col_name.remove('CloseTime')
  for i in col_name:
    for j in range(1,lag_cnt+1):
        dat[i+'_lag'+str(j)] = dat[i].shift(j)

  dat = dat.merge(tweet, how='left', on='CloseTime')        
  dat = dat.dropna(axis=0)

  train_x, train_y, valid_x, valid_y, test_x, \
    test_y, train_y_info, valid_y_info, test_y_info = generate_data(dat, col_name)
  # import tensorflow as tf
  # device_name = tf.test.gpu_device_name()
  # with tf.device('/device:GPU:0'):
  node_cnt1 = [32, 64, 128, 256]
  node_cnt2 = [32, 64, 128, 256]
  lr = [0.001]
  callback = EarlyStopping(monitor='loss', patience=5)

  para_dict = {'dense_node': node_cnt2,
          'lr': lr,
          'epochs':[100],
          'batch_size':[32, 64, 128],
          'dropout_rate':[0.1,0.2,0.4,0.6]}

  for layer_cnt in [2]:
    for k in range(layer_cnt): 
        para_dict['node'+str(k+1)] = eval('node_cnt'+str(k+1))

    if lag_cnt == 9:
      with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'_withTweet.json') as f:
        tmp_save = json.load(f)
      loss_dict = tmp_save['loss']
      val_loss_dict = tmp_save['val_loss']
      info = tmp_save['info']
      previous_cnt = len(loss_dict) 
    else:
      loss_dict = {}
      val_loss_dict = {}
      info = {}
      previous_cnt = 0

    iter_cnt = 0
    for k in para_dict['dropout_rate']:
      for i in node_cnt1:
        for n2 in node_cnt2:
          for j in para_dict['batch_size']:
            if iter_cnt < previous_cnt:
              iter_cnt = iter_cnt + 1
              print(iter_cnt)
              continue
            random.seed(iter_cnt+1)
            es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
            model = models.Sequential()
            model.add(layers.LSTM(i,input_shape=(train_x.shape[1], 1),
                                  kernel_regularizer='l2',return_sequences=True))
            model.add(layers.Dropout(k))
            model.add(layers.LSTM(i))
            model.add(layers.Dropout(k))
            model.add(layers.Dense(n2))
            model.add(layers.Dense(1))
            model.summary()

            model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
            history = model.fit(np.expand_dims(train_x, axis=2), train_y, 
                                epochs=200, 
                                batch_size=j, 
                                verbose=2,
                                callbacks = [es],
                                validation_data=(np.expand_dims(valid_x, axis=2), valid_y))
            history_dict = history.history


            # loss & accuracy
            info[iter_cnt] = 'node1='+str(i)+' node2='+str(n2)+' batch='+str(j)+' dropout='+str(k)
            loss_dict[iter_cnt] = history_dict['loss'][len(history_dict['loss'])-1]
            val_loss_dict[iter_cnt] = history_dict['val_loss'][len(history_dict['val_loss'])-1]
            print(info[iter_cnt]+' lag='+str(lag_cnt))
            if iter_cnt % 5 == 4:
              save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
              # save and download the result
              with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'_withTweet_cntOnly.json', 'w', encoding='utf-8') as f:
                json.dump(save_dic, f, ensure_ascii=False)

            iter_cnt = iter_cnt + 1

  save_dic = {'loss':loss_dict, 'val_loss':val_loss_dict, 'info':info}
  # save and download the result
  with open('drive/My Drive/result'+str(time_period)+'_lag'+str(lag_cnt)+'_withTweet_cntOnly.json', 'w', encoding='utf-8') as f:
    json.dump(save_dic, f, ensure_ascii=False)