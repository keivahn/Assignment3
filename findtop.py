# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo          # import the pymongo class to deal with the Mongo databases that we've created
import re               # import regx to help with the querying process

class FindTop:
# class for find the top in a database

    def FindReTweets(self, database, qty):
        # find the top qty of retweets in a given database

        # we create a query that we want to ignore, "RT" because we only want
        # to capture the original tweet and how often it was retweeted
        regx = re.compile("RT.*")

        # list of tweets sorted by retweet count and limited to the provided quantity
        # ignore the retweets, instead captured the original tweets
        tweets = list(database.tweetCollection.find({'text': {'$not': regx}}).sort('retweet_count', pymongo.DESCENDING).limit(qty))

        # iterate through the list and print the screen name, number of retweets, and the text of the tweet
        for record in tweets:
            print record['text']
            print record['user']['screen_name']
            print record['user']['location']
            print record['retweet_count']
            print "\n"

        # return the list of top retweets
        return list
