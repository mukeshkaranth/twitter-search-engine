import sys, getopt
import re
import json
import tweepy
import pandas as pd
from tweepy import OAuthHandler

# Authentication Keys
bearer_token = ""
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Dictionary to maintain a record of crawled tweet IDs.
duplicates = {}

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Function to extract tweets
def get_tweets(hashtag, count):
        # Authorization to consumer key and consumer secret
        auth = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_key,
            access_token_secret=access_secret,
            wait_on_rate_limit=True)

        print()
        print("Starting Tweepy API for "+hashtag)

        json_data = [[]]
        for tweet in tweepy.Paginator(auth.search_recent_tweets, query=hashtag+' lang:en -is:retweet', tweet_fields=['id', 'created_at', 'public_metrics', 'text', 'geo'], max_results=100).flatten(limit=int(count)):
                #Check to see if we are at a duplicate tweet before we can store it.
                if tweet and tweet.id not in duplicates.keys():
                        json_data = [[tweet.created_at, tweet.id, clean_tweet(tweet.text), tweet.public_metrics['like_count'], tweet.public_metrics['reply_count'], tweet.public_metrics['retweet_count'], tweet.public_metrics['quote_count'], tweet.geo['place_id'] if tweet.geo else>                        df = pd.DataFrame(json_data)
                        df.to_csv(str('/data/'+''.join(hashtag))+'CrawledTweetsData.csv', mode='a', index=False, header=False)
                        duplicates[tweet.id] = 1
        print('Results for '+ hashtag+ ' have been fetched!')


def main(argv):
        hashtagList = []
        limit = 1000

        #Command line argument handler
        opts, args = getopt.getopt(argv,"hl:c:",["list=","count="])
        for opt, arg in opts:
                if opt == '-h':
                        print ('TweetCrawler.py -l <[list-of-terms-to-search-on-twitter]> -c <max-number-of-tweets>')
                        sys.exit()
                elif opt in ("-l", "--list"):
                        hashtagList.append(arg)
                elif opt in ("-c", "--count"):
                        limit = arg
        if hashtagList and limit:
		    #hashtagList = ['bollywood', 'movies', 'film', 'cinema', 'movie', 'films', 'actor', 'actress', 'hollywood', 'dvd', 'bluray', 'streaming', 'boxoffice', 'oscars', 'goldenglobes','tollywood','sandalwood','recommendation','kollywood', 'review', 'imdb', 'must watch']
                #hashtagList = ['film', 'acting', 'review', 'films', 'actor', 'actress', 'hollywood', 'dvd', 'bluray', 'streaming', 'boxoffice', 'oscars', 'goldenglobe', '#movie', '#pathaan', 'bollywood', 'sandalwood', 'tollywood', 'kollywood', 'anime', 'drama', 'netflix', 'hulu>
                for hashtag in hashtagList:
                    try:
                        get_tweets(hashtag, limit)
                    except:
                        print("There was some error in collecting tweets.")

if __name__ == "__main__":
   main(sys.argv[1:])
