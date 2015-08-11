from __future__ import division     # import the division function from python 3 to get full float division

# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo                      # import the pymongo module to deal with the Mongo databases that we've created
import nltk                         # import the NLTK module to tokenize natural language
import tweetfetcher                 # import the tweetfetcher class to gather all tweets for a specified user
import json                         # import json module for exporting file format

# the starting point for all downloaded tweet files
FILE_NAME = "tweets"

class LexicalDiversity:
    # find the Lexical Diversity of a corpus, based on different criteria

    def userDiversity(self, database):
        # find the lexical diversity for a given user, the unique words divided by
        # the total number of words in that user's corpus

        # list all the records
        records = list(database.tweetCollection.find())

        # iterate through the database calculating the lexical diversity for each user
        for record in records:
            # gather the entire corpus of tweets using the userAllTweets method
            corpus = LexicalDiversity().userAllTweets(database, record['user']['screen_name'])

            # as long as we have a corpus of tweets to analyze
            if corpus <> "NA":
                # pass the corpus in the lexicalDiversity method to get the lexical diversity score
                score = LexicalDiversity().lexicalDiversity(corpus)

                # add a field for this user that states their lexical diversity
                record['lexical_diversity'] = score

                # save the updated collection
                database.tweetCollection.save(record)
            # if there is no corpus to analyze, we simply give the
            # user a score of 0 for lexical diversity
            else:
                record['lexical_diversity'] = 0
                # save the updated collection
                database.tweetCollection.save(record)

    def userAllTweets(self, database, user):
        # string all tweets for a given user all together

        # create a blank string for holding all the tweet text
        tweets = ""

        # find all tweets for a specified user using tweetfetcher
        tweetfetcher.TweetFetcher().searchUser(user)

        # load the appropriate JSON document with all the tweets
        try:
            file = open(FILE_NAME + "_" + str(user) + ".json","r")
            json_file = json.load(file)
            file.close()
        # if no file exists for the user, we return NA
        except:
            return "NA"

        # iterate through this JSON of tweets belonging to a particular user and
        # concatenate that tweet text with the string for holding all tweets
        for tweet in json_file:
            text = tweet['text'] + " "
            tweets = tweets + text

        # return the string of tweets
        return tweets

    def lexicalDiversity(self, corpus):
        # returns the lexical diversity of a string (unqiue words divided by total words)

        # convert the string to unicode to help with tokenization
        corpus = corpus

        # tokenize the string
        token_corpus = nltk.word_tokenize(corpus)

        # generate a frequency distribution of all words in the corpus
        frequency_distribution = nltk.FreqDist(token_corpus)

        # generate two variables to hold the total unique words and the total words
        unique_words = 0
        all_words = 0

        # loop through the frequency distribution to count the unique words and
        # all the words
        for word in frequency_distribution:
            unique_words = unique_words + 1
            all_words = all_words + frequency_distribution[word]

        # return the ratio of unqiue words to all words, unless the all words
        # value is 0, in which case return 0
        if all_words == 0:
            return 0
        else:
            print unique_words / all_words
            return unique_words / all_words
