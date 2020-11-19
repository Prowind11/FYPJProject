from flask import *
# from tmdbv3api import Movie
import pandas as pd
import os 
import sap_hana_data as data
import sap_hana_connection as conn
import requests
import MovieLens as movieLenFile

app = Flask(__name__)
app.secret_key = "SomeSecretKeyIKnow"
api_key = "d9ada7322b38e573bf5cd6e8d09091fe"
base_url = "https://api.themoviedb.org/3/movie/"
userData = []

@app.route('/')
def index():
    
    movieId = str(862)
    full_url = base_url + movieId + "?api_key=" + api_key + "&language=en-US"
    response = requests.get(full_url)
    movieInfo = response.json()

    # movieInfo = {
    #     "posterPath" : False,
    #     "id": 862,
    #     "belongs_to_collection": {
    #         "id":10194,
    #         "name":"Toy Story Collection",
    #         "poster_path":"/7G9915LfUQ2lVfwMEEhDsn3kT4B.jpg",
    #         "backdrop_path":"/9FBwqcd9IRruEDUrTdcaafOMKUq.jpg"
    #     }
    # print(movieInfo["belongs_to_collection"]["poster_path"])
    # }
    # movieInfo
    # print(movieInfo)
    # genresArray = []


    moviePosterPath = movieInfo["belongs_to_collection"]["poster_path"]

    moviePosterURL = "https://image.tmdb.org/t/p/w400" + moviePosterPath
    # print(moviePosterPath)
    movieName = movieInfo["belongs_to_collection"]["name"]
    genresArray = []

    for genre in movieInfo["genres"]:
        genresArray.append(genre["name"])

    totalTime = str(movieInfo["runtime"]) + "mins" 
    rating = movieInfo["vote_average"]
    # print(getUserData) -> [('84', 'Dinesh', 'none', 'none', 'none', 'none', 'none'), ('85', 'Dinesh', '', '', '', '', ''), ('86', 'Dinesh', '', '', '','', '')]
   
 
    return render_template('show_all_algorithms.html',totalTime = totalTime, rating = rating, movieName = movieName, genresArray = genresArray,moviePosterURL = moviePosterURL)


@app.route('/user_profile')
def user_profile():
    moviesIdArray = []
    tmdbIdArray = []

    movieNameArray = []
    moviePosterUrlArray= []
    moviesGenresArray = []
    totalTimeArray = []
    ratingArray = []


    global userData
    # print(len())
    ml = movieLenFile.MovieLens()
    # print(len(userData) == 0)
    itemToItemTopTenID = None
    userToUserTopTenID = None
    totalMovieCount = 0
    count = len(userData)
    # print(count == 0)
    if (count > 0) : 

        itemToItemTopTenName = userData[0][3]
        userToUserTopTenName = userData[0][4]

        itemToItemTopTenID = userData[0][5] # We retrieve it is a whole string
        userToUserTopTenID = userData[0][6]

        removeFirstLastChar = itemToItemTopTenID[1:-1]
        itemToItemTopTenIdString = removeFirstLastChar.replace("'","")
        itemToItemTopTenIDArray = itemToItemTopTenIdString.split(',')
 
        removeFirstLastChar = itemToItemTopTenName[1:-1]
        itemToItemTopTenNameString = removeFirstLastChar.replace("'","")
        itemToItemTopTenNameArray = itemToItemTopTenNameString.split(',')
        # print(itemToItemTopTenNameArray)

        for movieId in itemToItemTopTenIDArray:   
            # Remove space in the string
            movieIdTrimmed = movieId.strip() 
            tmdbIdArray.append(ml.getTmdbId(movieIdTrimmed))
            tmdbId = ml.getTmdbId(movieIdTrimmed)

            # print('tmdbid: ',tmdbId)
            
            movieId = str(tmdbId)
            full_url = base_url + movieId + "?api_key=" + api_key + "&language=en-US"
            response = requests.get(full_url)
            movieInfo = response.json()
            print(movieInfo)
            moviePosterURL = ""
            # print(movieInfo)
            moviePosterPath = movieInfo["belongs_to_collection"]
            if moviePosterPath is not None:
                moviePosterPath = movieInfo["belongs_to_collection"]["poster_path"]
                moviePosterURL = "https://image.tmdb.org/t/p/w400" + moviePosterPath
            else:
                moviePosterPath = movieInfo["backdrop_path"]
                moviePosterURL = "https://image.tmdb.org/t/p/w400" + moviePosterPath
            # print(movieInfo)
        #     print(moviePosterPath)

            # # # print(moviePosterPath)
            # movieName = movieInfo["belongs_to_collection"]["name"]
            genresArray = []

            for genre in movieInfo["genres"]:
                genresArray.append(genre["name"])

            for movieName in itemToItemTopTenNameArray:
                movieNameTrim = movieName.replace('"', '')
                movieNameArray.append(movieNameTrim)

            totalTime = str(movieInfo["runtime"]) + "mins" 
            rating = movieInfo["vote_average"]
            # movieNameArray.append(movieName)
            moviePosterUrlArray.append(moviePosterURL)
            moviesGenresArray.append(genresArray)
            totalTimeArray.append(totalTime)
            ratingArray.append(rating)

        totalMovieCount = len(moviePosterUrlArray)
        print(len(moviePosterUrlArray))

    return render_template('user_profile.html',movieNameArray = movieNameArray , moviePosterUrlArray = moviePosterUrlArray,moviesGenresArray= moviesGenresArray,totalTimeArray = totalTimeArray,ratingArray=ratingArray,count=totalMovieCount)


@app.route('/recommend_movie')
def recommend_movie():
    return render_template('recommend_movie.html')

@app.route('/get_recommend_movie',methods=["GET"])
def get_recommend_movie():

    return render_template('recommend_movie.html')

@app.route('/show_all_algorithms')
def show_all_algorithms():
    return render_template('show_all_algorithms.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    # if 'username' in session: # session is from flask, session is the browser window, so if close browser window totally, session data gone
    #         return redirect(url_for('login'))
    # else:
    #     if request.method == "POST":
    #         form = request.form
    #         username = data.login_user(form['username'], form['password'])
    #         if username is None:
    #             error = "You have entered an invalid username or password"
    #             print("Login Failed!")
    #         else:
    #             session['username'] = username
    #             return redirect(url_for('index'))
    #         flash(error)

    return render_template('login.html',isIndex=True)

@app.route('/register',methods=['GET', 'POST'])
def register():
    return render_template('register.html',isIndex=True)

@app.route('/search',methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        searchValue = request.form['search']
        if (searchValue.isnumeric()):
            # Search by ID 
            user = conn.get_user_data_by_id(searchValue)
            global userData 
            userData = []
            if user is not None:
                userData.append(user)
            return redirect(url_for('user_profile'))
        else:
            # Search by name string 
            print("nononoon")
          
    else:
        print("not searching")
    return render_template('user_profile.html',isIndex=True)

if __name__ == '__main__':
    ml = movieLenFile.MovieLens()

    ml.read_links_csv()
    ml.get_user_movie_watched()
    ml.read_item_names()
    # print("hello hello hello",ml.get_user_movie_watched().get("15"))
    # movieID_to_name, name_to_movieID, movieWithNameAndGenre = ml.read_item_names()
    # print(ml.getMovieId("Star Wars: Episode V - The Empire Strikes Back (1980)"))
    # print(ml.getMovieName("1"))
    app.run(debug=True)
