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
from src.db_fns import create_engine2, sql_db_to_df, add_user_to_group
from src.st_fns import check_un, rate_film_page, pref_page, gpref_page

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
        check_un(dict_cache['engine'], user_name, new_or_exist)
        dict_cache['user_confirmed'] = True
        dict_cache['user_name'] = user_name
    
    # Only show page options once username confimred
    if dict_cache['user_confirmed']:
        user_name_w.text(f'User name is : {dict_cache["user_name"]}')
        new_or_exist_w.empty()
        page = page_w.selectbox('Choose a page', ['Rate Films', 'Your Preferences', 'Group Preferences'])

    # Create group and/or add user to group
    add_user_to_group(dict_cache['engine'], dict_cache['user_name'], group_name)
    dict_cache['group_name'] = group_name
    
    # Page specific results to show
    if page == 'Rate Films':
        rate_film_page(dict_cache)
        
    elif page == 'Your Preferences':
        pref_page(dict_cache)
        
    elif page == 'Group Preferences':
        gpref_page(dict_cache)
        
    return


#%% Load film data from database
@st.cache()
def load_films():
    engine = create_engine2()
    df = sql_db_to_df(engine, 'W2W_Films')
    return df

#%% Persist data with dictionary
@st.cache(allow_output_mutation=True)
def cache_dict():
    temp_dict = {'engine' : create_engine2(),
                 'user_confirmed' : False,
                 'films_rated' : 0}
    temp_dict['W2W_Films'] = sql_db_to_df(temp_dict['engine'], 'W2W_Films')
    return temp_dict

#%% Run main function
if __name__ == '__main__':
    main()