'''
    File name: st_fns.py
    Author: Henry Letton
    Date created: 2021-02-10
    Python Version: 3.8.3
    Desciption: Any functions used in the streamlit page layout
'''

#%% Import any modules required for the functions
import streamlit as st
from src.db_fns import user_name_exist, group_name_exist, add_user, add_user_to_group

#%% Require user and group names before loading rest of site
def check_names(engine, user_name, group_name, new_or_exist):
    
    
    if user_name == '':
        st.warning('Please input a user name.')
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
            st.write('New user created')

    if group_name == '':
        st.warning('Please input a group name.')
        st.stop()

    if not group_name_exist(engine, group_name):
        add_user_to_group(engine, user_name, group_name)
        
    return
    