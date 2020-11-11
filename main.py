from flask import *
# from tmdbv3api import Movie

import os 
import sap_hana_data as data
import sap_hana_connection as conn
import requests

app = Flask(__name__)
api_key = "d9ada7322b38e573bf5cd6e8d09091fe"
base_url = "https://api.themoviedb.org/3/movie/"

@app.route('/')
def index():
    movieId = str(862)
    full_url = base_url + movieId + "?api_key=" + api_key + "&language=en-US"
    response = requests.get(full_url)
    movieInfo = response.json()

    # genresArray = []
    moviePosterPath = movieInfo["belongs_to_collection"]["poster_path"]
    moviePosterURL = "https://image.tmdb.org/t/p/w400" + moviePosterPath
    # print(moviePosterPath)
    movieName = movieInfo["belongs_to_collection"]["name"]
    genresArray = []

    for genre in movieInfo["genres"]:
        genresArray.append(genre["name"])
        # print("genre:",genre["name"])
    # print(genresArray)

    totalTime = str(movieInfo["runtime"]) + "mins" 
    rating = movieInfo["vote_average"]
    # data.__insert_table()
    # # print(moviePosterPath)
    # conn.__insert_table()
    conn.__update_table()
    # getUserData = conn.get_user_data()
    # print(getUserData) -> [('84', 'Dinesh', 'none', 'none', 'none', 'none', 'none'), ('85', 'Dinesh', '', '', '', '', ''), ('86', 'Dinesh', '', '', '','', '')]
   
    # results = data.__retrieve_user_table()
    # print(results) 
    # allData = data.__retrieve_table()
    # print(allData)
    #    <!-- Image -->
    #     <!-- Movie Name -->
    #     <!-- Genre -->

    #     <!-- Total Time -->
    #     <!-- Ratings -->

    # print(movieInfo)
    # if (response == 200){
    #     print(request)
    # }

    return render_template('show_all_algorithms.html',totalTime = totalTime, rating = rating, movieName = movieName, genresArray = genresArray,moviePosterURL = moviePosterURL)


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')


@app.route('/recommend_movie')
def recommend_movie():
    return render_template('recommend_movie.html')

@app.route('/get_recommend_movie',methods=["GET"])
def get_recommend_movie():

    return render_template('recommend_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
