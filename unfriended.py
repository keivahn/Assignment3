# Alex Smith
# W205 - Storing and Retrieving Data
# Assignment #3

import pymongo          # import the pymongo module to deal with the Mongo databases that we've created
import findfollowers    # import findfollowers class to find the remaining of an individual

# limit of the number of users we want to research
LIMIT = 10

class Unfriend():
    # class to find the number of unfollower's compared to an original list of findfollowers

    def unfriended(self, collection):
        # compare a collection that contains a list of followers with the current number of followers
        # and return the list of user ids of those who unfollowed the individual

        # create a dictionary to hold the individual and all their followers
        originalFollowers = {}

        # loop through each record in the collection, adding the user and the number
        # of followers to the dictionary
        for record in collection.limit(LIMIT):
            originalFollowers[record['user_id']] = record['followers']

        # create a new dictionary to hold the individual's current followers
        currentFollowers = {}

        # loop through each user_id in the dictionary to find their current followers
        # and add the list of friends to the dictionary
        for user in originalFollowers:
            friends = findfollowers.FindFollowers().accessTwitter(user)
            currentFollowers[user] = friends

        # compare the friend lists to find which friends dropped out
        droppedFollowers = dropped(originalFollowers, currentFollowers)

    def dropped(self, originalDictionary, newDictionary):
        # compare two dictionaries of followers to identify which followers
        # exist in the first dictionary but not in the second

        # create a new dictionary to store dropped followers
        dropped = {}

        # iterate through both dictionaries, adding to dropped followers when
        # a followers is present in the first but not the second
        for user in originalDictionary:

            # create a list to hold dropped followers
            droppedList = []

            # look at each follower of a user
            for follower in originalDictionary[user]:

                # if the follower is not in the list in the new dictionary,
                # add the follower to the droppedList
                if follower not in newDictionary[user]:
                    droppedList.append(follower)

            # create a new dictionary entry for the user and the dropped followers
            dropped[user] = droppedList
