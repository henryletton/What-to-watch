'''
    File name: app.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Central script for dashboard
'''

#%% Import required modules and functions
import streamlit as st
import pandas as pd
from datetime import datetime
from src.db_fns import create_engine2, sql_db_to_df, add_user_to_group, add_user_rating
from src.st_fns import check_un

#%% Create any objects here that need to persist outside of page refreshes
engine = create_engine2() # DB connection

#%% Funciton for site
def main():
    
    # Persistent dictionary object (within session not all sessions)
    dict_cache = cache_dict()
    print(dict_cache)
    
    # Input options for user
    new_or_exist_w = st.sidebar.empty()
    new_or_exist = new_or_exist_w.radio('Are you a new or exisitng user:', ['New','Existing'])
    user_name_w = st.sidebar.empty()
    user_name = user_name_w.text_input('User name', '')
    group_name = st.sidebar.text_input('Group name', '')
    # Page sidebar serves as page navigator for user
    page_w = st.sidebar.empty()
    
    # Handling of user name
    if not dict_cache['user_confirmed']:
        check_un(engine, user_name, new_or_exist)
        dict_cache['user_confirmed'] = True
        dict_cache['user_name'] = user_name
    
    # Only show page options once username confimred
    if dict_cache['user_confirmed']:
        user_name_w.text(f'User name is : {dict_cache["user_name"]}')
        new_or_exist_w.empty()
        page = page_w.selectbox('Choose a page', ['Rate Films', 'Your Preferences', 'Group Preferences'])

    # Create group and/or add user to group
    add_user_to_group(engine, dict_cache['user_name'], group_name)

    #st.write('Stopping here')
    #st.stop()
    
    # Film information
    W2W_Films = load_films()
    
    
    if page == 'Rate Films':
        st.header('Rate Films')
        st.write('Please select your preferences for movies below')
        
        # Save space to display film info
        film_info_w = st.empty()
        film_desc_w = st.empty()
        
        # Film info to be stored with rating
        idx = dict_cache['films_rated']
        #current_film_title = W2W_Films['title'][idx]
        #current_film_year = int(W2W_Films['year'][idx])
        current_film_key = W2W_Films['film_key'][idx]
        
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
            add_user_rating(engine, dict_cache["user_name"], 
                            current_film_key, rating)
            # Increment ensures different film after refresh
            dict_cache['films_rated'] = dict_cache['films_rated'] + 1
        
        # Film info shown needs to be after the films_rated has been incremented
        idx = dict_cache['films_rated']
        next_film_title = W2W_Films['title'][idx]
        next_film_year = int(W2W_Films['year'][idx])
        next_film_description = W2W_Films['description'][idx]
        
        film_info_w.write(f'Do you want to watch {next_film_title}, released in {next_film_year}')
        film_desc_w.write(next_film_description)
        
        #st.dataframe(W2W_Films)
        
    elif page == 'Your Preferences':
        st.header('Your Preferences')
        st.write('If you wish to erase all previous preferences, then click _Erase_ below.')
        if st.button('Erase'):
            st.write(f'Preferences deleted at {datetime.now()}')
        else:
            pass
        st.write(f'Below shows the current preferences for {user_name}')
        
    elif page == 'Group Preferences':
        if group_name == '':
            st.warning('Group preferences will appear once you specify a group')
            st.stop()
        st.title('Group Preferences')
        st.write(f'Below shows preferences for films in the group {group_name}')



#%% Load film data from database
@st.cache()
def load_films():
    engine = create_engine2()
    df = sql_db_to_df(engine, 'W2W_Films')
    return df

#%% Persist data with dictionary
@st.cache(allow_output_mutation=True)
def cache_dict():
    temp_dict = {'user_confirmed' : False,
                 'films_rated' : 0}
    return temp_dict

#%% Run main function
if __name__ == '__main__':
    main()