import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import numpy as np

ratingsPath = 'C:/Users/182381j/Desktop/dataset/ml-latest-small-100k/ratings.csv'
moviesPath = 'C:/Users/182381j/Desktop/dataset/ml-latest-small-100k/movies.csv'
movieID_to_name = {}
name_to_movieID = {}
movieWithNameAndGenre = {}
testSubject = '84'
k = 10

# sim_options = {'name': 'cosine',
#                'user_based': True
#             }

class MovieLens:

    def loadMovieLensLatestSmall(self):
        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        data = Dataset.load_from_file(ratingsPath, reader=reader)

        # with open(moviesPath, newline='', encoding='ISO-8859-1') as csvfile:
        #     movieReader = csv.reader(csvfile)
        #     next(movieReader)  #Skip header line
        #     for row in movieReader:
        #         movieID = int(row[0])
        #         movieName = row[1]
        #         movieID_to_name[movieID] = movieName
        #         name_to_movieID[movieName] = movieID

        return data

    def read_item_names(self):
#     """Read the u.item file from MovieLens 100-k dataset and return two
#     mappings to convert raw ids into movie names and movie names into raw ids.
#     """
        with open(moviesPath, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                gettingGenresArray = line.split(',')
                genres = gettingGenresArray[2].split('|')

                line = line.split('|')
                movieID = line[0].split(',')[0]
                movieName = line[0].split(',')[1]

                movieID_to_name[movieID] = movieName
                name_to_movieID[movieName] = movieID

                movieWithNameAndGenre[movieID] = {}
                movieWithNameAndGenre[movieID]['movieName'] = movieName
                movieWithNameAndGenre[movieID]['genres'] = genres

        return movieID_to_name, name_to_movieID, movieWithNameAndGenre
    
    def getMovieName(self,movieID):
        if movieID in movieID_to_name:
            return movieID_to_name[movieID]
