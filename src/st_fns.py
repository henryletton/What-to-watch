'''
    File name: st_fns.py
    Author: Henry Letton
    Date created: 2021-02-10
    Python Version: 3.8.3
    Desciption: Any functions used in the streamlit page layout
'''

#%% Import any modules required for the functions
import streamlit as st
from src.db_fns import *
import regex as re
import datetime
import random

#%% Require user and group names before loading rest of site
def check_un(engine, user_name, new_or_exist):
    if user_name == '':
        st.warning('Please input a user name.')
        st.stop()
        
    if bool(re.search('[^A-Za-z0-9]', user_name)):
        st.warning('User names must only contain numbers or letters')
        st.stop()
        
    if user_name_exist(engine, user_name):
        if new_or_exist == 'New':
            st.warning('User name already exists, choose another.')
            st.stop()
            
    else:
        if new_or_exist == 'Existing':
            st.warning('User name does not exist.')
            st.stop()
        else:
            add_user(engine, user_name)
            st.warning('New user created')
    return
    
#%% Details of rating films page
def rate_film_page(dict_cache):

    st.header('Search for Film')
    search_placeholder = st.empty()
    search_query = search_placeholder.text_input('Film name', '')
    genre_query = st.text_input('Genre', '')
    df_search = search_film(dict_cache["engine"], search_query, genre_query)
    num_results = len(df_search.index)
    
    # Check if search query is not empty
    if search_query:
        if 10 >= num_results > 1:
            st.write("More than one result found, please narrow down search query from options below")
            st.write(df_search)
        elif num_results == 0:
            st.write("No results found")
        elif num_results > 10:
            st.write("Too many results found to display")
        else:
            selected_key = df_search["film_key"].values[0]
            search_film_desc_w = st.empty()
            
            # Film info to be stored with rating
            search_current_film_key = selected_key
        
            # Save space to display film info
            search_film_info_w = st.empty()
            search_film_desc_w = st.empty()
            
            search_film_title = df_search["title"].values[0]
            search_film_year = int(df_search["year"].values[0])
            search_film_description = df_search["description"].values[0]
            
            search_film_info_w.write(f'Do you want to watch {search_film_title}, released in {search_film_year}')
            search_film_desc_w.write(search_film_description)
            
            # Text rating is mapped to number
            # Only stored once user clicks a button
            rating = -99
            if st.button('Yes, looks rad!', key="search_good"):
                rating = 5
            if st.button('No, I have taste!', key="search_bad"):
                rating = 0
            if st.button('Skip', key="search_skip"):
                rating = -1
            if rating != -99:
                # Create new hash for new random film
                dict_cache['random_hash'] += random.randrange(-n_films, n_films)
                add_user_rating(dict_cache['engine'], dict_cache["user_name"], search_current_film_key, rating)
               
            # Clear search once search has found a film
            search_query = search_placeholder.text_input('Film name', value='', key=1)
        
    else:
        st.write("Please enter film to search for")
        
   
    st.header('Rate Films')
    st.write('Please select your preferences for movies below')
    
    # Save space to display film info
    film_info_w = st.empty()
    film_desc_w = st.empty()
    
    # Get films rated by group, but not rated by user
    n_films = get_film_count(dict_cache['engine'])
    urated_films_df = get_user_rated_films(dict_cache["engine"], dict_cache["user_name"])
    grated_films_df = get_group_rated_films(dict_cache["engine"], dict_cache["group_name"])
    
    df_merge = urated_films_df.merge(grated_films_df, on='film_key', how='outer', indicator=True)
    films_to_rate = df_merge.loc[df_merge['_merge'] == "right_only"]["film_key"].tolist()
    if films_to_rate:
        rand_film = random.choice(films_to_rate)
        films_to_rate.remove(rand_film)
        w2w_films = dict_cache['W2W_Films']
        # Convert datframe to series
        film_row = w2w_films.loc[w2w_films['film_key'] == rand_film].squeeze()
    else:
        rand_row_idx = dict_cache['random_hash'] % n_films
        film_row = dict_cache['W2W_Films'].iloc[rand_row_idx] 
    # Film info to be stored with rating
    
    current_film_key = film_row['film_key']
    
    # Text rating is mapped to number
    # Only stored once user clicks a button
    rating = -99
    if st.button('Yes, looks rad!', key="random_good"):
        rating = 5
    if st.button('No, I have taste!', key="random_bad"):
        rating = 0
    if st.button('Skip', key="random_skip"):
        rating = -1
    if rating != -99:
        add_user_rating(dict_cache['engine'], dict_cache["user_name"], 
                        current_film_key, rating)
        # Create new hash for new random film
        dict_cache['random_hash'] += random.randrange(-n_films, n_films)
    
    # Film info shown needs to be after the hash has changed
    next_film_title = film_row['title']
    
    next_film_year = int(film_row['year'])
    next_film_description = film_row['description']
     
    film_info_w.write(f'Do you want to watch {next_film_title}, released in {next_film_year}')
    film_desc_w.write(next_film_description)
    
    return

#%% Details of user preferences page
def upref_page(dict_cache):
    
    st.header('Your Preferences')
    st.write('If you wish to erase all previous preferences, then click _Erase_ below.')
    if st.button('Erase'):
        st.write(f'Preferences deleted at {datetime.datetime.now()}')
    else:
        pass
    st.write(f'Below shows the current preferences for {dict_cache["user_name"]}')
    rated_films_df = get_user_rated_films(dict_cache["engine"], dict_cache["user_name"])
    st.write(rated_films_df.drop(["film_key"], axis=1))
    return

#%% Details of group preferences page
def gpref_page(dict_cache):
    
    if dict_cache["group_name"] == '':
        st.warning('Group preferences will appear once you specify a group')
        st.stop()
    st.title('Group Preferences')
    st.write(f'Below shows preferences for films in the group {dict_cache["group_name"]}')
    grated_films_df = get_group_rated_films(dict_cache["engine"], dict_cache["group_name"])
    st.write(grated_films_df.drop(["film_key"], axis=1))
    return


