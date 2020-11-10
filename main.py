from flask import *
# from tmdbv3api import Movie

import os 
import sap_hana_data as data
import requests

app = Flask(__name__)
api_key = ""
base_url = "https://api.themoviedb.org/3/movie/"

@app.route('/')
def index():
    movieId = str(862)
    full_url = base_url + movieId + "?api_key=" + api_key + "&language=en-US"
    response = requests.get(full_url)
    movieInfo = response.json()

    # genresArray = []
    moviePosterPath = movieInfo["belongs_to_collection"]["poster_path"]
    # print(moviePosterPath)
    movieName = movieInfo["belongs_to_collection"]["name"]
    genresArray = []

    for genre in movieInfo["genres"]:
        genresArray.append(genre["name"])
        # print("genre:",genre["name"])
    # print(genresArray)

    totalTime = str(movieInfo["runtime"]) + "mins" 
    rating = movieInfo["vote_average"]
    print(moviePosterPath)

    #    <!-- Image -->
    #     <!-- Movie Name -->
    #     <!-- Genre -->

    #     <!-- Total Time -->
    #     <!-- Ratings -->

    # print(movieInfo)
    # if (response == 200){
    #     print(request)
    # }

    return render_template('show_all_algorithms.html')


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
