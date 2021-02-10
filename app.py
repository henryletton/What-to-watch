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
from src.db_fns import create_engine2, sql_db_to_df
from src.st_fns import check_names

#%% Create any objects here that need to persist outside of page refreshes
engine = create_engine2() # DB connection
dict_cache= {} # Dictionary for forks in page layout
dict_cache['user_confirmed'] = False

#%% Funciton for site
def main():
    
    # Persistent dictionary object (within session not all sessions)
    #dict_cache = cache_dict()
    print(dict_cache)
    
    # Input options for user
    new_or_exist = st.sidebar.radio('Are you a new or exisitng user:', ['New','Existing'])
    user_name = st.sidebar.text_input('User name', '')
    group_name = st.sidebar.text_input('Group name', '')
    # Page sidebar serves as page navigator for user
    page = st.sidebar.empty()
    
    # Handling of username name and group
    if not dict_cache['user_confirmed']:
        check_names(engine, user_name, group_name, new_or_exist)
        dict_cache['user_confirmed'] = True
    
    # Only show page options once 
    if dict_cache['user_confirmed']:
        page = page.selectbox('Choose a page', ['Rate Films', 'Your Preferences', 'Group Preferences'])

    #st.write('Stopping here')
    #st.stop()
    
    if page == 'Rate Films':
        st.header('Rate Films')
        st.write('Please select your preferences for movies below')
        st.write('If you wish to erase all previous preferences, then click _Erase_ below.')
        if st.button('Erase'):
            st.write(f'Preferences deleted at {datetime.now()}')
        else:
            pass
        st.dataframe(load_films())
        
    elif page == 'Your Preferences':
        st.header('Your Preferences')
        st.write(f'Below shows the current preferences for {user_name}')
        
    elif page == 'Group Preferences':
        if group_name == '':
            st.warning('Group preferences will appear once you specify a group')
            st.stop()
        st.title('Group Preferences')
        st.write(f'Below shows preferences for films in the group {group_name}')



#%% Load film data from database and cahce
@st.cache
def load_films():
    engine = create_engine2()
    df = sql_db_to_df(engine, 'W2W_Films')
    return df

#%% Run main function
if __name__ == '__main__':
    main()