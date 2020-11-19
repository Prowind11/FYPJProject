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
from surprise import KNNBaseline
from surprise import accuracy
from surprise import dump
from collections import defaultdict
from operator import itemgetter

# Import class
from MovieLens import MovieLens

# Import the whole file to access the global variable
import MovieLens as ml

sim_options = {'name': 'pearson_baseline', 'user_based': False}
# ml = MovieLens()
# data = ml.loadMovieLensLatestSmall()
# movieID_to_name, name_to_movieID, movieWithNameAndGenre = ml.read_item_names()
# trainSet = data.build_full_trainset()


def findSimilarItem(movieName):
    ml = MovieLens()
    data = ml.loadMovieLensLatestSmall()
    moviesArray = []
    movieID_to_name, name_to_movieID, movieWithNameAndGenre, movieNameArray = ml.read_item_names()
    trainSet = data.build_full_trainset()
    algo = KNNBaseline(sim_options=sim_options)
    algo.fit(trainSet)

    toy_story_raw_id = name_to_movieID[movieName]
    toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)

    # Retrieve inner ids of the nearest neighbors of Toy Story.
    toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)

    # Convert inner ids of the neighbors into names.
    toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id)
                        for inner_id in toy_story_neighbors)
    toy_story_neighbors = (movieID_to_name[rid]
                        for rid in toy_story_neighbors)

    for movie in toy_story_neighbors:
        moviesArray.append(movie)
    
    return moviesArray