'''
    File name: st_fns.py
    Author: Henry Letton
    Date created: 2021-02-10
    Python Version: 3.8.3
    Desciption: Any functions used in the streamlit page layout
'''

#%% Import any modules required for the functions
import streamlit as st
from src.db_fns import user_name_exist, add_user
import regex as re

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
    
#%% 

