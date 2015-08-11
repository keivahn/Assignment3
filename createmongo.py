# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo                  # import the module to deal with Mongo databases
import json                     # import the JSON module because the tweet files are JSONs
import datetime                 # import datetime module to access JSON files from assignment #2
import boto                     # import boto in case we choose to download the file from S3
from boto.s3.key import Key     # import the key function from boto to make the downloading script clearer

FILE_NAME = "tweets"

class CreateMongo:
# class for creating Mongo databases

    def CreateMongoLive(self,query1,query2):
        # create a new mongo database based on two queries

        # initialize the connection with MongoDB
        conn = self.test()

        # create a new database
        database = conn['MyMongoDB_Live']

        # create a new collection to store the tweets
        tweetCollection = database.tweetCollection

        # open the json files as readable and close the original files
        file1 = open(FILE_NAME + "_" + str(query1) + ".json","r")
        json_file1 = json.load(file1)
        file1.close()
        file2 = open(FILE_NAME + "_" + str(query2) + ".json","r")
        json_file2 = json.load(file2)
        file2.close()

        # insert each tweet into the Mongo database
        list_of_files = [json_file1,json_file2]
        for file in list_of_files:
            for tweet in file:
                tweetCollection.insert(tweet)

        # return the database
        return database

    def CreateMongoOld(self, query1, query2, begin, end):
        # create a new Mongo database based on the previous assignment

        # initialize the connection with MongoDB
        conn = self.test()

        # create a new database
        database = conn['MyMongoDB_Old']

        # create a new collection for inserting the tweets
        tweetCollection = database.tweetCollection

        # loop through the files from the former assignment and add them to MongoDB
        # limit the count of tweets
        list_of_queries = [query1,query2]
        for query in list_of_queries:
            current = begin
            while current <= end:
                # initialize the count to 0 to limit the amount of tweets due to capacity
                # constraints on the harddrive

                # open each file
                file_name = "tweets_" + query + "_" + str(current) + ".json"
                file = open(file_name,"r")
                json_file = json.load(file)

                # add each tweet to the Mongo DB collection
                for tweet in json_file:
                    tweetCollection.insert(tweet)
                    print "Adding tweet:"
                    print tweet['text']

                # close the file
                file.close()

                # increment current to the next day
                current = current + datetime.timedelta(days = 1)
                
        # return the database to the calling function
        return database


        # code to pull the data from S3 (if I had correctly uploaded my data to S3 in assignment 2)
        # because I did not correctly upload my code, I've commented this out
        # AWS credentials
        # AWS_ACCESS_KEY_ID = '...'
        # AWS_SECRET_ACCESS_KEY = '...'
        # bucket_name = "keivahn-w205-assignment2"

        # connect to Amazon Web Services (AWS) and pull the bucket
        # conn_aws = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        # bucket = conn_aws.get_bucket(bucket_name)

        # pull all files in the bucket and download to our local directory
        # bucket_list = bucket.list()
        # for file in bucket_list:
            # file_name = str(file.key)
            # file.get_contents_to_filename(file_name)
        # now that we have the file downloaded, we can simply loop through the file like above
        # and add each tweet to our MongoDB using the insert function (just as above, in the same method)

    def createMongoFollowers(self, user_id, followers):
        # create a mongo database to hold a twitter user_id and a list of the individual's followers

        # initialize the connection with MongoDB
        conn = self.test()

        # create a new database
        database = conn['MyMongoDB_Followers']

        # create a new collection to store the followers
        tweetFollowers = database.followers

        # return the database
        return database

    def createMongoBasic(self, json_file, name):
        # create a mongo database with a specified name from a JSON file

        # initialize the connection with MongoDB
        conn = self.test()

        # create a new database
        database = conn[name]

        # create a new collection to store the records
        records = database.records

        # open the file and load it as a JSON
        file = open(json_file, "w")
        json_file = json.load(file)

        # iterate through the JSON file adding each line to the database
        for record in json_file:
            records.insert(record)

    def test(self):
        # create the connection with MongoDB so that you can create
        # and modify Mongo databases

        try:
            conn=pymongo.MongoClient()
            print "Connected!"
            return conn
        except pymongo.errors.ConnectionFailure, e:
           print "Connection failed : %s" % e
