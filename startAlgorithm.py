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

# Import class
from MovieLens import MovieLens

# Import the whole file to access the global variable
import MovieLens as ml
df_data = pd.read_csv(ml.ratingsPath, encoding = 'Windows-1252')
total_user = df_data.userId.unique()
total_number_of_user = len(df_data.userId.unique())
print(total_number_of_user)

# k = 10 
# userORItemBoolean = [True,False]
# itemToItemTopTen = []
# UserToUserTopTen = []

# predictions_knnBasic_item, algo_knnBasic = dump.load('C:/Users/182381j/Desktop/dump_file_100k_KNNBasic_item_to_item')
# predictions_knnBasic_user, algo_knnBasic = dump.load('C:/Users/182381j/Desktop/dump_file_100k_KNNBasic_user_to_user')

# # This matrix consists of all the user similarity value to the test user
# simsMatrix_item_to_item = predictions_knnBasic_item.compute_similarities()
# simsMatrix_user_to_user = predictions_knnBasic_user.compute_similarities()
# # print(simsMatrix)

# ml = MovieLens()
# data = ml.loadMovieLensLatestSmall()
# movieID_to_name, name_to_movieID, movieWithNameAndGenre = ml.read_item_names()
# trainSet = data.build_full_trainset()

# # simsMatrix = predictions_knnBasic.compute_similarities()
# # print(simsMatrix)
# for userId in total_user:
#     testSubject = str(userId)
#     conn.__insert_user_table(testSubject)
#     itemToItemTopTen = []
#     UserToUserTopTen = []


#     # Maybe can put all the prediction in the dump file so we can use in the future 
#     # file_name = os.path.expanduser('~/dump_file_100k_KNNBasic')
#     # dump.dump(file_name, predictions,algo=model)
#     # predictions_knnBasic, algo_knnBasic = dump.load('C:/Users/182381j/Desktop/dump_file_100k_KNNBasic')

#     for x in range(2):

#         # Get top N similar users to our test subject
#         # (Alternate approach would be to select users up to some similarity threshold - try it!)
#         testUserInnerID = trainSet.to_inner_uid(testSubject)
#         if x == 0:
#             similarityRow = simsMatrix_item_to_item[testUserInnerID]
#         else:
#             similarityRow = simsMatrix_user_to_user[testUserInnerID]

#         print(similarityRow)
#         similarUsers = []
#         # enumerate add a number inside the tuple, (userID:1,similarityValue: 1) - if 1 is similar, 0 not similar
#         for innerID, score in enumerate(similarityRow):
#             if (innerID != testUserInnerID):
#                 similarUsers.append( (innerID, score) )
                
#         # Top 10 Neighbour closest to the test subject
#         kNeighbors = heapq.nlargest(k, similarUsers, key=lambda t: t[1])

#         # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
#         candidates = defaultdict(float)
#         for similarUser in kNeighbors:
#             innerID = similarUser[0]
#             userSimilarityScore = similarUser[1]
#             # A list of similar rated things
#             theirRatings = trainSet.ur[innerID]
#             for rating in theirRatings:
#                 # print(rating)
#                 # rating[0] - movieID ??? , rating[1] - movie ratings
#                 candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore
            
#         # Build a dictionary of stuff the user has already seen
#         watched = {}
#         for itemID, rating in trainSet.ur[testUserInnerID]:
#             watched[itemID] = 1

#         pos = 1

#         # print(candidates.items())
#         # Itemgetter(1) get the second item of the tuple,similarity value)(movieID,similarity value)
#         for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
#             # print('itemId:',itemID)
#             # print('ratingSum:',ratingSum)
#             if not itemID in watched:
#                 # print(type(itemID))
#                 movieID = trainSet.to_raw_iid(itemID)
#                 # print(movieID)
#                 # print(ml.getMovieName(str(movieID)), ratingSum)
#                 movieName = ml.getMovieName(str(movieID))
#                 if x == 0:
#                     itemToItemTopTen.append(movieName)
#                 else:
#                     UserToUserTopTen.append(movieName)
#                 pos += 1
#                 if (pos > 10):
#                     break

#         # print(itemToItemTopTen)
#         # print(UserToUserTopTen)

#         #  Update 
#     print(itemToItemTopTen,UserToUserTopTen,userId)
#     conn.__update_user_table(str(itemToItemTopTen),str(UserToUserTopTen),str(userId))
# param_grid = {'n_epochs': [20, 30], 'lr_all': [0.005, 0.010],
#               'n_factors': [50, 100]}
# gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)