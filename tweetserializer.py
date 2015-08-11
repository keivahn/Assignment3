# Alex Smith
# MIDS - W205
# Assignment #3

import json # import json module for exporting file format

FILE_NAME = "tweets"

class TweetSerialize:
    # class to write the tweets from Twitter to a file

    # basic assumptions
    count = 0
    out = None
    first = False
    current_tweet_count = 0


    def start(self, query):
        # bring the program to life

        # increment the self counter by 1
        self.count = self.count + 1

        # create a new file based on the query name
        file_name = FILE_NAME + "_" + str(query) + ".json"

        # open the file in self.out
        self.out = open(file_name,"w")

        # write a new line, set first to true, and set count to 0
        self.out.write("[\n")
        self.first = True
        self.current_tweet_count = 0

    def end(self):
        # end the program

        # confirm that the program has actually begun, add 2 blank lines to end
        # and close the file
        if self.out is not None:
            self.out.write("\n]\n")
            self.out.close()

        # get out of the file
        self.out = None

    def write(self,tweet):
        # write the tweets to our file

        # if this is not the first tweet, write a new line with a comma seperator
        if not self.first:
            self.out.write(",\n")

        # set the first indicator back to False
        self.first = False

        # write the tweet to the file as a json and increment the tweet count
        self.out.write(json.dumps(tweet._json).encode('utf8'))
        self.current_tweet_count = self.current_tweet_count + 1
