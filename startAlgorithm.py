import pandas as pd
import numpy as np
#import seaborn as sns # never use much
#import matplotlib.pyplot as plt # never use much
import os 
import heapq
import csv
import sys # never use
import re # never use
import sap_hana_connection as conn

from hana_ml import dataframe
from hana_ml.dataframe import ConnectionContext

from surprise.model_selection import GridSearchCV
from surprise import SVD
from surprise import Dataset
from surprise import Reader 
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
from surprise import dump
from collections import defaultdict
from operator import itemgetter

from MovieLens import MovieLens

testSubject = '84'
k = 10 
userORItemBoolean = [True,False]
itemToItemTopTen = []
UserToUserTopTen = []

for x in userORItemBoolean:
 
    sim_options = {'name': 'cosine',
                'user_based': x
                }

    ml = MovieLens()
    data = ml.loadMovieLensLatestSmall()
    movieID_to_name, name_to_movieID, movieWithNameAndGenre = ml.read_item_names()

    trainSet = data.build_full_trainset()
    model = KNNBasic(sim_options=sim_options)
    predictions = model.fit(trainSet)

    # Maybe can put all the prediction in the dump file so we can use in the future 
    # file_name = os.path.expanduser('~/dump_file_100k_KNNBasic')
    # dump.dump(file_name, predictions,algo=model)
    # predictions_knnBasic, algo_knnBasic = dump.load('C:/Users/182381j/Desktop/dump_file_100k_KNNBasic')

    # This matrix consists of all the user similarity value to the test user
    simsMatrix = model.compute_similarities()
    # print(simsMatrix)


    # Get top N similar users to our test subject
    # (Alternate approach would be to select users up to some similarity threshold - try it!)
    testUserInnerID = trainSet.to_inner_uid(testSubject)

    similarityRow = simsMatrix[testUserInnerID]

    similarUsers = []
    # enumerate add a number inside the tuple, (userID:1,similarityValue: 1) - if 1 is similar, 0 not similar
    for innerID, score in enumerate(similarityRow):
        if (innerID != testUserInnerID):
            similarUsers.append( (innerID, score) )
            
    # Top 10 Neighbour closest to the test subject
    kNeighbors = heapq.nlargest(k, similarUsers, key=lambda t: t[1])

    # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
    candidates = defaultdict(float)
    for similarUser in kNeighbors:
        innerID = similarUser[0]
        userSimilarityScore = similarUser[1]
        # A list of similar rated things
        theirRatings = trainSet.ur[innerID]
        for rating in theirRatings:
            # print(rating)
            # rating[0] - movieID ??? , rating[1] - movie ratings
            candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore
        
    # Build a dictionary of stuff the user has already seen
    watched = {}
    for itemID, rating in trainSet.ur[testUserInnerID]:
        watched[itemID] = 1

    pos = 1

    # print(candidates.items())
    # Itemgetter(1) get the second item of the tuple,similarity value)(movieID,similarity value)
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        # print('itemId:',itemID)
        # print('ratingSum:',ratingSum)
        if not itemID in watched:
            # print(type(itemID))
            movieID = trainSet.to_raw_iid(itemID)
            # print(movieID)
            # print(ml.getMovieName(str(movieID)), ratingSum)
            movieName = ml.getMovieName(str(movieID))
            if x == True:
                UserToUserTopTen.append(movieName)
            else:
                itemToItemTopTen.append(movieName)
            pos += 1
            if (pos > 10):
                break

# print(itemToItemTopTen)
# print(UserToUserTopTen)

#  Update 
conn.__update_user_table(str(itemToItemTopTen),str(UserToUserTopTen))
# param_grid = {'n_epochs': [20, 30], 'lr_all': [0.005, 0.010],
#               'n_factors': [50, 100]}
# gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)