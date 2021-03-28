'''
    File name: st_fns.py
    Author: Henry Letton
    Date created: 2021-02-10
    Python Version: 3.8.3
    Desciption: Any functions used in the streamlit page layout
'''

#%% Import any modules required for the functions
import streamlit as st
from src.db_fns import user_name_exist, add_user, add_user_rating
import regex as re
import datetime

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
    
    st.header('Rate Films')
    st.write('Please select your preferences for movies below')
    
    # Save space to display film info
    film_info_w = st.empty()
    film_desc_w = st.empty()
    
    # Film info to be stored with rating
    idx = dict_cache['films_rated']
    #current_film_title = W2W_Films['title'][idx]
    #current_film_year = int(W2W_Films['year'][idx])
    current_film_key = dict_cache['W2W_Films']['film_key'][idx]
    
    # Text rating is mapped to number
    # Only stored once user clicks a button
    rating = -99
    if st.button('Yes, looks rad!'):
        rating = 5
    if st.button('No, I have taste!'):
        rating = 0
    if st.button('Skip'):
        rating = -1
    if rating != -99:
        add_user_rating(dict_cache['engine'], dict_cache["user_name"], 
                        current_film_key, rating)
        # Increment ensures different film after refresh
        dict_cache['films_rated'] = dict_cache['films_rated'] + 1
    
    # Film info shown needs to be after the films_rated has been incremented
    idx = dict_cache['films_rated']
    next_film_title = dict_cache['W2W_Films']['title'][idx]
    next_film_year = int(dict_cache['W2W_Films']['year'][idx])
    next_film_description = dict_cache['W2W_Films']['description'][idx]
    
    film_info_w.write(f'Do you want to watch {next_film_title}, released in {next_film_year}')
    film_desc_w.write(next_film_description)
    
    #st.dataframe(W2W_Films)
    return

#%% Details of user preferences page
def pref_page(dict_cache):
    
    st.header('Your Preferences')
    st.write('If you wish to erase all previous preferences, then click _Erase_ below.')
    if st.button('Erase'):
        st.write(f'Preferences deleted at {datetime.now()}')
    else:
        pass
    st.write(f'Below shows the current preferences for {dict_cache["user_name"]}')
    return

#%% Details of group preferences page
def gpref_page(dict_cache):
    
    if dict_cache["group_name"] == '':
        st.warning('Group preferences will appear once you specify a group')
        st.stop()
    st.title('Group Preferences')
    st.write(f'Below shows preferences for films in the group {dict_cache["group_name"]}')
    return


