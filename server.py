import re
import tweepy
import pandas as pd
import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def search(text_query):
    count = 150
    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search, q=text_query).items(count)
        tweets = filter(lambda x: 'RT @' not in x.text, tweets) 

    # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text, tweet.user.screen_name]
                       for tweet in tweets]

    # Creation of dataframe from tweets list
        tweets_df = pd.DataFrame(tweets_list, columns=['Created At', 'Tweet Id', 'Tweet Text', "User Id"])
        return tweets_df
    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
    
def timeline(count):
    # fetching the statuses 
    statuses = api.home_timeline(count=count) 
  
# printing the screen names of each status 
    for status in statuses:
        result = search(status.text)
        if (not result.empty):
          print(result)

timeline(25)
