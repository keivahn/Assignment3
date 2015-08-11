# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo                      # import the pymongo class to deal with the Mongo databases that we've created
import boto                         # import the boto module to send items to S3 and download them
import bson                         # import the bson module to help export and import mongo db databases
from boto.s3.key import Key         # import the Key function of the boto module to set the specific file in the bucket
import datetime                     # import the datetime module to add a time stamp to the back up
import createmongo                  # import the createmongo module to create a mongo database from a back up

# credentials for accessing my AWS bucket
AWS_ACCESS_KEY = "..."
AWS_SECRET_ACCESS_KEY = "..."
BUCKET_NAME = "keivahn-w205-assignment3"

# file name is back up for descriptive purposes
FILE_NAME = "backup"

# current provides a time stamp for the back up
CURRENT = datetime.date.today()

class MongoS3:
    # class to connect mongo databases to S3

    def sendS3(self, database):
        # export a Mongo database as a JSON file and send to S3

        # create the back up file
        backup_file = MongoS3().createJSON(database)

        # create a connection
        connection = MongoS3().createConnection()

        # upload the specific file
        bucket = connection.get_bucket(BUCKET_NAME)
        Key(bucket).set_contents_from_file(backup_file, rewind = True)

        # close the file to cleanly end the program
        backup_file.close()

    def retrieveS3(self, datestamp):
        # download a backup JSON from S3 based from what ever date
        # the user specifies

        # create the file name based on the user supplied date
        file_name = FILE_NAME + "_" + str(datestamp) + ".json"

        # create a connection
        connection = MongoS3().createConnection()

        # get the key for the given file and download the file
        # keeping the same file name
        key = bucket.get_key(file_name)
        key.get_contents_to_filename(file_name)

        # add the file to a mongo database and name the database based on the date
        createmongo.CreateMongo().createMongoBasic(file_name, datestamp)

    def createConnection(self):
        # establish a connection with AWS using credentials in constants
        connection = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY,host='s3-us-west-1.amazonaws.com')
        return connection

    def createJSON(self, database):
        # create a JSON for uploading to S3
        # create a JSON file and open it
        file_name = FILE_NAME + "_" + str(CURRENT) + ".json"
        file = open(file_name,"w")

        # write the opening bracket
        file.write("[")

        # pull all records in the database
        records = list(database.tweetCollection.find())

        # iterate through the list writing each record to a
        # new line in the JSON file
        for record in records:
            file.write(str(record) + "\n")

        # write the closing bracket
        file.write("]")

        # close the file to end this method
        file.close()

        # open the file as readable before returning it
        file = open(file_name,"r+")

        # return the file to upload it
        return file
