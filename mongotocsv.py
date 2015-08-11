# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo          # import the pymongo class to deal with the Mongo databases that we've created

class MongotoCSV:
    # class to create CSV files from Mongo databases

    def userDiversity(self, file_name, database, limit_qty):
        # create a 2 column CSV file based on the user id and the lexical
        # diversity score

        # create a file based on the file name provided
        file = MongotoCSV().createFile(file_name)

        # create an iterable list of records that is also ordered
        list = database.tweetCollection.find().sort('lexical_diversity', pymongo.DESCENDING).limit(limit_qty)

        # iterate through the list, printing to the CSV file
        for record in list:
            file.write(record['user']['screen_name'] + ", " + str(record['lexical_diversity']) + "\n")

        # close the file
        file.close()

    def createFile(self, file_name):
        # create a new CSV file based on a specified file name

        # add the CSV extension
        file_name = file_name + ".csv"

        # open the file
        file = open(file_name,'w')

        return file
