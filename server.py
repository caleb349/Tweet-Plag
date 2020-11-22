from datetime import datetime
import re
import tweepy
import pandas as pd
import time
from flask import Flask, json, request, Response
consumer_key = "q2odiAzgwoTWodRDtKa6pRqtI"
consumer_secret = "zNQ8SZH0oEVEprQlGNF0BtKrluTYUG1KkautdmkJeWvTgzPMU3"
access_token = "3413666200-OTGCcLNnd7miQnL60IibnddRLCgsfMXaKfeCgnW"
access_token_secret = "Tz45UeQam241P8oq9OSJLaw0r1NQiNwB7wET0EZqCpAOF"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
app = Flask(__name__)


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
        tweets_df = pd.DataFrame(tweets_list, columns=[
                                 'Created At', 'Tweet Id', 'Tweet Text', "User Id"])
        return tweets_df
    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


def check_plag(df, tweet_id):
    date_time = ""
    date_time2 = ""
    for tweet in df:
        if tweet[1] == tweet_id:
            date_time = tweet[0]
            date_time = datetime.strptime(date_time, "%m-%d-%Y %H:%M:%S")
    
    for tweet in df:
        if (len(tweet[0]) >= 17):
            date_time2 = datetime.strptime(tweet[0], "%m-%d-%Y %H:%M:%S")
        if not tweet[1] == tweet_id and date_time > date_time2:
            return True

    return False


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


@app.route('/result/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        tweet_id = request.form['url']
        tweet = request.form['summary']
        searching = search(tweet)
        check = check_plag(searching, tweet_id)
        if not check:
            return "Original Tweet"
        else:
            return "Plagarized Tweet"


if __name__ == "__main__":
    app.run()