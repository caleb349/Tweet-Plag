
import tweepy
import pandas as pd
import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

text_query = 'Could you please make a free live streaming of the Thanksgiving Day Parade available to all Peacock account holders?'
count = 150
try:
 # Creation of query method using parameters
 tweets = tweepy.Cursor(api.search,q=text_query).items(count)
 
 # Pulling information from tweets iterable object
 tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
 
 # Creation of dataframe from tweets list
 tweets_df = pd.DataFrame(tweets_list, columns=['Created At','Tweet Id', 'Tweet Text'])
 
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)


