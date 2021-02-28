'''
    File name: db_fns.py
    Author: Henry Letton
    Date created: 2021-01-26
    Python Version: 3.8.3
    Desciption: Any functions interacting with the database
'''

#%% Import any modules required for the functions
from sqlalchemy import create_engine 
import pandas as pd
import os
import hashlib

#%% Load system variables from .env file, not required on Heroku
from dotenv import load_dotenv
load_dotenv()

#%% Function to establish connection to database
def create_engine2(sql_user = os.environ.get("sql_user"),
                   sql_pw = os.environ.get("sql_pw"),
                   sql_db = os.environ.get("sql_db")):
    
    # Link to database
    db_url = f'mysql+mysqlconnector://{sql_user}:{sql_pw}@{sql_db}'
    engine = create_engine(db_url)
    
    return engine

#%% Function to read complete table from database
def sql_db_to_df(engine,
                 table_name):
    
    # Connect to database - this works but outputs an sql error for some reason
    #engine.connect()
    # Run query for table
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', engine)
    
    return df

#%% Function to insert film row
def insert_film_db(engine,
                   details,
                   update = False,
                   query = """W2W_Films (title, year, description, platform, tag, film_key)
                        VALUES (%s, %s, %s, %s, %s, %s)"""):
    
    # Updating requires updating old row, else it will be skipped
    if update:
        query_full = f"REPLACE INTO {query}"
    else:
        query_full = f"INSERT IGNORE INTO {query}"
    
    # Add film key to tuple
    str_to_hash = str(details[0]) + str(details[1])
    film_key = hashlib.md5(str_to_hash.encode()).hexdigest()
    details_list = list(details)
    details_list.append(film_key)
    details2 = tuple(details_list)
    
    # Connext to db
    engine.connect()                        
    
    # Insert/ignore/replace film row
    with engine.begin() as cnx:
        cnx.execute(query_full, details2)
    
    return

#%% Check if username exists
def user_name_exist(engine, user_name):
    
    # Connext to db
    engine.connect()
    
    # Get user table where username is a match
    query = f"SELECT * FROM W2W_Users WHERE user_name = '{user_name}'"
    un_df = pd.read_sql_query(query, engine)
    
    # If nomatch then false, otherwise true
    if len(un_df.index) == 1:
        return True
    
    elif len(un_df.index) == 0:
        return False
    
    else:
        print('Error: duplicate user names')
        return True

#%% Check if group exists
def group_name_exist(engine, group_name):
    
    # Connext to db
    engine.connect()
    
    # Get user table where username is a match
    query = f"SELECT * FROM W2W_Groups WHERE group_name = '{group_name}'"
    un_df = pd.read_sql_query(query, engine)
    
    # If nomatch then false, otherwise true
    if len(un_df.index) == 1:
        return True
    
    elif len(un_df.index) == 0:
        return False
    
    else:
        print('Error: duplicate user names')
        return True

#%% Add new user
def add_user(engine, user_name):
    
    # Connext to db
    engine.connect()
    
    # Create user key
    user_key = hashlib.md5(user_name.encode()).hexdigest()
    
    # Insert user name in
    query = "INSERT IGNORE INTO W2W_Users (user_key, user_name) VALUES (%s, %s)"
    with engine.begin() as cnx:
        cnx.execute(query, (user_key, user_name))
        
    return

#%% Add new group
def add_group(engine, group_name):
    
    # Do not add blank group
    if group_name == '':
        return
    
    # Connext to db
    engine.connect()
    
    # Create group key
    group_key = hashlib.md5(group_name.encode()).hexdigest()
    
    # Insert user name in
    query = "INSERT IGNORE INTO W2W_Groups (group_key, group_name) VALUES (%s, %s)"
    with engine.begin() as cnx:
        cnx.execute(query, (group_key, group_name))
        
    return

#%% Add user to group
def add_user_to_group(engine, user_name, group_name):
    
    # Do not add blank group
    if group_name == '':
        return
    
    # Connext to db
    engine.connect()
    
    # Add group, if not exist
    add_group(engine, group_name)
    
    # Create unique keys
    user_key = hashlib.md5(user_name.encode()).hexdigest()
    group_key = hashlib.md5(group_name.encode()).hexdigest()
    
    # Insert user and group in
    query = "INSERT IGNORE INTO W2W_Group_User_Mapping (group_key, user_key) VALUES (%s, %s)"
    with engine.begin() as cnx:
        cnx.execute(query, (group_key, user_key))
        
    return

#%% Add rating 
def add_user_rating(engine, user_name, film_key, rating):
    
    # Connext to db
    engine.connect()
    
    # Create user key
    user_key = hashlib.md5(user_name.encode()).hexdigest()
    
    # Insert user and group in
    query = "REPLACE INTO W2W_User_Rating (user_key, film_key, rating) VALUES (%s, %s, %s)"
    with engine.begin() as cnx:
        cnx.execute(query, (user_key, film_key, rating))
        
    return


#%% Testing
# engine = create_engine2()
# test_name = 'test1'
# test_gname = 'gtest1'
# test_user = user_name_exist(engine, test_name)
# add_user(engine, test_name)
# test_user2 = user_name_exist(engine, test_name)

# test_group = group_name_exist(engine, test_gname)
# add_user_to_group(engine, test_name, test_gname)
# test_group2 = group_name_exist(engine, test_gname)

# add_user_rating(engine, 'test1', 'test2', 2021, 5)
