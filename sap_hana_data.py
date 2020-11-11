from hana_ml import dataframe
from hana_ml import ConnectionContext
from hdbcli import dbapi

# Method 1 
# def __get_connection():
#     conn = dataframe.ConnectionContext(
#         address='cdab230a-29d1-4a66-ab93-eb0ec219ed8b.hana.trial-us10.hanacloud.ondemand.com', 
#         port='443', 
#         user='MOVIE_PROJECT_HDI_DB_1_4T01X86GTZG3PJFBDJJ4FGMZR_RT', 
#         password='Rh0wQ9.bsJ.2NG_K2x73D.0J06Hh8UTNIE_FAohpy9M5ocviZiyFN8WgR_uq6.kPX0fMR-ASiJrm7za9_uNs_hAsceXRW_qM9vBSTlWbUYPv1dozzBHgukbN4m_6WkaU',
#         encrypt='true', sslValidateCertificate='false')

#     return conn

# Method 2 
def __get_connection():
    conn = dbapi.connect(
        address="cdab230a-29d1-4a66-ab93-eb0ec219ed8b.hana.trial-us10.hanacloud.ondemand.com",
        port="443",
        encrypt="true",
        user="MOVIE_PROJECT_HDI_DB_1_4T01X86GTZG3PJFBDJJ4FGMZR_RT",
        password='Rh0wQ9.bsJ.2NG_K2x73D.0J06Hh8UTNIE_FAohpy9M5ocviZiyFN8WgR_uq6.kPX0fMR-ASiJrm7za9_uNs_hAsceXRW_qM9vBSTlWbUYPv1dozzBHgukbN4m_6WkaU'  
    ) 
    return conn

def __retrieve_table():
    conn = __get_connection()
    sql = "select * from MOVIE_PROJECT_HDI_DB_1.RATINGS"
    df_pushdown = conn.sql(sql)
    results = df_pushdown.collect()
    print(results)
    return results 

# Retrieve User Table
def __retrieve_user_table():
    conn = __get_connection()
    sql = "select * from MOVIE_PROJECT_HDI_DB_1.USERS"
    df_pushdown = conn.sql(sql)
    results = df_pushdown.collect()
    print(len(results))
    return results 


def __insert_table():
    userID = "84"
    userName = "Dinesh"
    itemToItem = ""
    userToUser = ""
    watched_movies = ""
    merged_algorithms = ""
                                                                   
    conn = __get_connection()
    # sql = "INSERT INTO MOVIE_PROJECT_HDI_DB_1.USERS VALUES (?,?,?,?,?,?,?)," + "("+userID,userName,itemToItem,userToUser,watched_movies,merged_algorithms+")"
    # sql =  "INSERT INTO MOVIE_PROJECT_HDI_DB_1.USERS VALUES(" + userID,userName,itemToItem,userToUser,watched_movies,merged_algorithms + ")"
    # print(sql)
    # df_push = conn.sql(sql)
    
