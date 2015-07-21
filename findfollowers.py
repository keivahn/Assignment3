# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo          # import the pymongo module to deal with the Mongo databases that we've created
import tweepy           # import Tweepy module to help with accessing the Twitter followers
import createmongo      # import createmongo class to create our mongo database

# credentials to access Twitter account
consumer_key = "..."
consumer_secret = "..."
access_token = "..."
access_token_secret = "..."

class FindFollowers:
# find the Twitter followers based on criteria

    def findfollowers(self, collection):
        # find the followers of everyone in a given collection

        # create a new Mongo database for storing the users and their friends
        db_followers = createmongo.CreateMngo().createMongoFollowers()

        # iterate through the collection, identifying every record, and passing the
        # user id for every tweet into method, accessTwitter and then insert each
        # user_id with the number of followers in the database
        for record in collection:
            followers = FindFollowers().accessTwitter(record['user']['id'])
            db_followers.followers.insert({'user_id': record['user']['id'], 'followers_count': record['user']['followers_count'],'followers': followers})

        # return the collection of followers
        return db_followers.followers.find().sort('followers_count', pymongo.DESCENDING)

    def accessTwitter(self, user_id):
        # find the followers of a given user

        # apply credentials using tweepy module
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # use the tweepy api to limit the rate of downloads and not
        # be banned
        self.api = tweepy.API(auth_handler = auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

        # create a blank list for storing the friends
        friends = []

        # iterate through a cursor for all the followers of a given user
        for follower in tweepy.Cursor(self.api.followers_ids, id = user_id).pages():
            friends.extend(page)

        # return the list of friends
        return friends
