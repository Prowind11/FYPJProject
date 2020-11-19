from surprise import KNNBasic
from surprise import accuracy
from surprise import dump

# Import class
from MovieLens import MovieLens

# Import the whole file to access the global variable
import MovieLens as ml
import os 
import pandas as pd
userORItemBoolean = [True,False]
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
    file_tail_name = ""
    if x:
        file_tail_name = "_user_to_user"
    else:
        file_tail_name = "_item_to_item"
    file_name = os.path.expanduser('~/dump_file_100k_KNNBasic' + file_tail_name)
    dump.dump(file_name, predictions,algo=model)
 
 
predictions_knnBasic, algo_knnBasic = dump.load('C:/Users/182381j/Desktop/dump_file_100k_KNNBasic_item_to_item')
simsMatrix = predictions_knnBasic.compute_similarities()
print(simsMatrix)


