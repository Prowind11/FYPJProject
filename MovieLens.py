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
linksPath = 'C:/Users/182381j/Desktop/dataset/ml-latest-small-100k/links.csv'
movieID_to_name = {}
name_to_movieID = {}
movieWithNameAndGenre = {}
movieID_to_tmdbID = {}

movieUserWatched = {}
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
    
    
    # links.csv 
    def read_links_csv(self):
#     """Read the u.item file from MovieLens 100-k dataset and return two
#     mappings to convert raw ids into movie names and movie names into raw ids.
#     """
        #  1. Get Movie Watched
        #  2. get the movie id 
        #  3. get the tmdb id of each user watched movie
        with open(linksPath, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                data = line.split(',')
         
                # if (data[0] == )
                movieId = data[0]
                tmdb_id = data[2]
                movieID_to_tmdbID[movieId] = tmdb_id
        return movieID_to_tmdbID
                # line = line.split('|')
                # movieID = line[0].split(',')[0]
                # movieName = line[0].split(',')[1]

                # movieID_to_name[movieID] = movieName
                # name_to_movieID[movieName] = movieID

                # movieWithNameAndGenre[movieID] = {}
                # movieWithNameAndGenre[movieID]['movieName'] = movieName

    def get_user_movie_watched(self):
        with open(ratingsPath, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                row = line.split(',')

                userId = row[0]
                movieId = row[1]

                if not userId in movieUserWatched:
                    movieUserWatched[userId] = {}

            # "
            #     movieUserWatched = {
            #         "1" : {
            #             '1': tmdb_id,
            #             '2': tmdb_id
            #         },

            #     }
            # "
                tmdb_id = movieID_to_tmdbID.get(movieId)
                # movieUserWatched[userId] = {}
                movieUserWatched[userId][movieId] = tmdb_id
            # print(len(line))
            movieUserWatched.pop('userId',None)
        return movieUserWatched
     
    def getMovieName(self,movieID):
        if movieID in movieID_to_name:
            return movieID_to_name[movieID]

ml = MovieLens()
print(len(ml.get_user_movie_watched()))

ml.read_links_csv()
print("hello hello hello",ml.get_user_movie_watched().get("15"))