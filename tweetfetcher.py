# Alex Smith
# MIDS - W205
# Assignment #3

import tweepy           # module to help with acquiring data from twitter
import signal           # module to get a async signals from the system
import threading        # locking module to prevent corrupted data
import tweetserializer  # import the function to write the tweets
import threading        # locking module that prevents half written tweets
import datetime         # import the datetime module to separate json files by date
import time             # import time module to help tweepy sleep

# sleep time; the time the application should rest if it encounters an error
# before continuing on, in seconds
SLEEP_TIME = 1000

# sleep time for the user query, we use a shorter sleep time because the
# the error is likely to be due to an invalid user rather than a stop by Twitter
SLEEP_TIME_USER = 5

# choose a sample size for the number of tweets gathered if we search for tweets
# by user
TWEET_SAMPLE = 200

# current date to ensure that we pull no more than a weeks worth of data
CURRENT = datetime.date.today()
RANGE = datetime.timedelta(days=6)

class TweetFetcher:
    # class to download the tweets based on the specified parameters

    def __init__(self):

        # initialize the lock to prevent half written tweets
        self._lock = threading.RLock()

        # credentials to access twitter account
        consumer_key = "..."
        consumer_secret = "..."
        access_token = "..."
        access_token_secret = "..."

        # apply credentials using tweepy module
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # use the tweepy api to limit the rate of downloads and not
        # be banned
        self.api = tweepy.API(auth_handler = auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

        # call a function to define tasks in the case of user interrupt
        signal.signal(signal.SIGINT, self.interrupt)

    def interrupt(self,signum,frame):
        # interrupt the function, but first finish getting the last tweet

        # use the threading module to finish gathering the last tweet
        print "Please wait, application is gathering last tweet and closing..."
        with self._lock:
            self.serializer.end()

        # exit with code 1 to indicate abnormal exit
        exit(1)

    def search(self, query):
        # search for a certain term, query

        # create a serializer and create the json to which it will write
        self.serializer = tweetserializer.TweetSerialize()
        self.serializer.start(query)

        # search the cursor for the search term q within a 1 week range and write the
        # appropriate tweet using serializer's write function
        # use the lock function to ensure the complete tweet is written
        # we limit to searching English tweets to avoid troublesome characters
        try:
            for tweet in tweepy.Cursor(self.api.search,q=query, since = CURRENT - RANGE, until = CURRENT, lang = "en").items():
                with self._lock:
                    self.serializer.write(tweet)

        # when there is an error sleep for 1000 seconds, necessary because
        # sometimes Twitter shuts off the connection
        except BaseException as e:
            print 'Error, program failed: '+ str(e)
            time.sleep(SLEEP_TIME)

        # end the serializer to close and save the file
        self.serializer.end()

    def searchUser(self, user_id):
        # search for tweets by a certain user_id

        # create a serializer and create the json to which it will write
        self.serializer = tweetserializer.TweetSerialize()
        self.serializer.start(user_id)

        # search through the cursor
        try:
            for tweet in tweepy.Cursor(self.api.user_timeline, id = user_id, lang = "en").items(TWEET_SAMPLE):
                with self._lock:
                    self.serializer.write(tweet)

        # when there is an error sleep for 1000 seconds, necessary because
        # sometimes Twitter shuts off the connection
        except BaseException as e:
            print 'Error, program failed: '+ str(e)
            print 'Will attempt to continue after sleeping for 5 seconds'
            time.sleep(SLEEP_TIME_USER)

        # end the serializer to close and save the file
        self.serializer.end()
