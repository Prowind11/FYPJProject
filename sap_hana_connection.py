from hdbcli import dbapi

def __get_connection():
    conn = dbapi.connect(
        address="cdab230a-29d1-4a66-ab93-eb0ec219ed8b.hana.trial-us10.hanacloud.ondemand.com",
        port="443",
        encrypt="true",
        user="MOVIE_PROJECT_HDI_DB_1_4T01X86GTZG3PJFBDJJ4FGMZR_RT",
        password='Rh0wQ9.bsJ.2NG_K2x73D.0J06Hh8UTNIE_FAohpy9M5ocviZiyFN8WgR_uq6.kPX0fMR-ASiJrm7za9_uNs_hAsceXRW_qM9vBSTlWbUYPv1dozzBHgukbN4m_6WkaU'  
    ) 
    return conn


def get_user_data():
    cursor = __get_connection().cursor()
    cursor.execute("select * from MOVIE_PROJECT_HDI_DB_1.USERS")
    rows = cursor.fetchall()
    user_data = []
    if len(rows) > 0:
        for row in rows:
            user_data.append(row)
        return user_data
            # print(type(row)) -> <class 'pyhdbcli.ResultRow'>
            # print(row) -> ('86', 'Dinesh', '', '', '', '', '')
    return None

def __insert_table():
    # Need To Check if the userID is taken or not , if not will crash
    userID = "86"
    userName = "Dinesh"
    itemToItem = ""
    userToUser = ""
    svd = ""
    watched_movies = ""
    merged_algorithms = ""
                                                                   
    cursor = __get_connection().cursor()
    sql = "INSERT INTO MOVIE_PROJECT_HDI_DB_1.USERS VALUES (?,?,?,?,?,?,?)"
    cursor.execute(sql,(userID,userName,itemToItem,userToUser,svd,watched_movies,merged_algorithms))


def __update_table():
    watchmovieArray =  str(["testing"])
    print(watchmovieArray)
    # userId = str(85)
    cursor = __get_connection().cursor()
    sql = "UPDATE MOVIE_PROJECT_HDI_DB_1.USERS SET WATCHED_MOVIES=?  WHERE USERID = ?"
    cursor.execute(sql,(watchmovieArray,84))

def __update_user_table(itemToItemTopTen,UserToUserTopTen):
    cursor = __get_connection().cursor()
    sql = "UPDATE MOVIE_PROJECT_HDI_DB_1.USERS SET ITEMTOITEM_TOP_TEN_ITEM = ? ,USERTOUSER_TOP_TEN_ITEM=? WHERE USERID = ?"
    cursor.execute(sql,(itemToItemTopTen,UserToUserTopTen,84))

#     cursor.execute("UPDATE MOVIE_PROJECT_HDI_DB_1.USERS SET WATCHED_MOVIES='[handsome]' WHERE USERID = 84")
# # Write data
# parameters = [
#   (1, 2, "3"),
#   (4, 5, "6"),
# ]

# query = 'INSERT INTO schema.t1 VALUES (?, ?, ?)'
# cursor.executemany(query, parameters)