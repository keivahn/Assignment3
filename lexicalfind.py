# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo          # import the pymongo class to deal with the Mongo databases that we'll be creating
import createmongo      # import the createmongo class to create the actual Mongo database
import urllib           # impor the urllib module to handle search queries for Twitter's API
import tweetfetcher     # import the class to pull the tweets from Twitter's REST API
import datetime         # import datetime module to access JSON files from assignment #2
import findtop          # import findtop30 class to find the top 30 retweets
import lexicaldiversity # import lexicaldiversity class to find the lexical diversity of different users
import findfollowers    # import the find followers class to find users' followers
import unfriended       # import the unfriended class to find which followers stopped following a user
import mongotocsv       # import the mongotocsv class to create a CSV plot of lexical diversities
import mongos3          # import the mongos3 class to back up the mongo database on AWS S3

# queries that we intend to use to search Twitter
QUERY1 = "#NBAFinals2015"
QUERY2 = "#Warriors"

# beginning and ending dates for assignment #2
BEGIN = datetime.date(2015, 6, 14)
END = datetime.date(2015, 6, 20)

# we want the top 30 retweets, rather than hard-code, we add
# this to our preliminary assumptions
TOP_RETWEET = 30

# we want the lexcial diversity plot for just the
# top 30 users
TOP_LEXICAL = 30

# convert the queries to a format accessible to Twitter's search
query1 = urllib.quote_plus(QUERY1)
query2 = urllib.quote_plus(QUERY2)

# call an application to search Twitter's REST API and return
# tweets matching the queries, writing to two JSON files
tweetfetcher.TweetFetcher().search(query1)
tweetfetcher.TweetFetcher().search(query2)

# import the json files into a Mongo database, db_restT, from our most
# recent query
db_restT = createmongo.CreateMongo().CreateMongoLive(query1,query2)

# import the json files into a Mongo database, db_tweets, from
# assignment #2
db_tweets = createmongo.CreateMongo().CreateMongoOld(query1, query2, BEGIN, END)

# find the top thirty retweets from the database, db_tweets
top_retweets = findtop.FindTop().FindReTweets(db_tweets, TOP_RETWEET)

# compute the lexical diversity of the tweets in the database, db_restT
lexicaldiversity.LexicalDiversity().userDiversity(db_restT)

# call a function to plot the the lexical diversity of the top 30 users
# to a CSV file
mongotocsv.MongotoCSV().userDiversity("Lexical Plot", db_restT, TOP_LEXICAL)

# find all the followers for those with the top 30 retweets
db_followers = findfollowers.FindFollowers().findfollowers(top_retweets)

# one week later, we un-comment this code to find which followers stopped following the top ten users
#unfriended = unfriended.Unfriend().unfriended(db_followers)
#print unfriended

# store a back up of db_tweets and db_restT to S3
mongos3.MongoS3().sendS3(db_restT)
mongos3.MongoS3().sendS3(db_tweets)
