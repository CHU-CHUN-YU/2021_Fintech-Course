--- fintech_price.py —
1. You need to install talib-binary first.
2. Access to your google cloud drive to get the price data json file.
3. Choose your price data’s time periods, 7200 for 2 hours, 14400 for 4 hours,
            21600 for 6 hours etc.
4. Variable selection (Currently setting will be listed below)
* Lags: half days, one days, one and half days, two days 
* Adding technical index: MA5, MA10, MA20, KD, MACD, RSI, ADX, ADXR, Bollinger Band
* Twitter Data: 
1. Top/Average count
2. NLTK positive/negative count
3. BERT score and Top/Average count
4. NLTK score and Top/Average count
5. BERT/NLTK score, Top/Average count, and NLTK positive/negative count
                *** Top/Average count refers to the count of like, retweet, quote and reply of top1  
      popular article and average among all articles
            4-1. We try to apply PCA to lag one and half day and two days; 10, 20, 30, 40 
        components are selected for hypertuning.
5. Split the dataset into training, validation and test sets. The periods are 2021/1/1-2021/7/31, 2021/8/1-2021/9/30 and 2021/10/1-2021/11/11, respectively.
6. Do min-max transformation through “min_max” function while keep the min/max information for prediction price recovery
7. Tune hyperparameters and record the loss of each hyperparameter set.
* Layers: LSTM1 + dropout1 + LSTM2 + dropout2 + 2 dense layers
* Node counts: 32, 64, 128, 256
* Optimizer: Adam with learning rate 0.0005, 0.001, 0.0015, 0.002
* Dropout rate: 0.1, 0.2, 0.4, 0.6
* Batch Size: 32, 64, 128
* EarlyStopping: patience on validation loss with step 5 and 10
* Epoch: 200 (all of them stop before 200 with earlystopping callback)
8. Retrain the model with training and validation data after best hyperparameters are determined. Then evaluate their performance on the prediction set.
–- end of fintech_price.py —


–- data_retrieval.py —
1. Create directory “tweets/tweets_timeline” and “candles/btcusdt”
2. Obtain your cryptowatch api keys and put in “cw.api_key”.
3. Obtain your twitter api keys and put in “twauth”.
4. Run the code with command “python3 data_retrieval.py”
5. You should find tweets and candlestick .json files in the directories created in 1.
–- end of data_retrieval.py —


-– tweets_preprocess_and_nltk.py —
1.load nltk “vader_lexicon”
2.read tweets from “tweets/tweets_timeline”
3.filter tweets contain bitcoin-related words
4.tweets preprocess and save to “filtertweets_clean/timeline”
5. read  price data from “candles/btcusdt/14400”,“candles/btcusdt/14400”,“candles/btcusdt/21600”,“candles/btcusdt/43200” and calculate close price change 
6.read tweets data from  “filtertweets_clean/timeline” and make polarity score using SIA from nltk 
7.filter tweets by |sent score|>0 
8.merge tweets by 4hr,6hr,12hr time period
9.make polarity score again
10.merge tweets data with ‘Close_change’, ‘up_down’ in price data
11.save merged dataset to  “tweets_with_price’’
–- end of tweets_preprocess_and_nltk.py —


–pre-train bert model.py—-
1.Load pre-trained BERT Model from the Transformer library of Hugging Face. Use “bert-base-uncase” consists of  12-layer、768-hidden、 12-heads、110M parameters.
2. Split the whole dataset into training (2021.01~2021.07), validation (2021.08~2021.09), testing(2021.10~2021.11.11) sets.
3. Train model. Create a BertForSequenceClassification model for classifier tasks.
4.To Fine-tune BertForSequenceClassification model, we applied AdamW as optimizer and used the following Hyper-Parameters.In Particular, we replaced Tanh activation as sigmoid. 
* Batch size: 16 or 32
* Learning rate (Adam): 5e-5, 3e-5 or 2e-5
* Number of epochs: 2, 3, 4,10,20
5. Finally, we evaluated its performance on the validation set.
* Unpack our data and load onto the GPU
* Forward pass
* Compute loss and accuracy rate over the validation set
—-- end of pre-train bert model.py—-------------