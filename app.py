'''
    File name: app.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Central script for dashboard
'''

import streamlit as st
from datetime import datetime

def main():
    user_name = st.sidebar.text_input('User name', '')
    group_name = st.sidebar.text_input('Group name', '')
    page = st.sidebar.selectbox('Choose a page', ['Rate Films', 'Your Preferences', 'Group Preferences'])

    if user_name == '':
        st.warning('Please input a user name.')
        st.stop()

    if page == 'Rate Films':
        st.header('Rate Films')
        st.write('Please select your preferences for movies belwow')
        st.write('If you wish to erase all previous preferences, then click _Erase_ below.')
        if st.button('Erase'):
            st.write(f'Preferences deleted at {datetime.now()}')
        else:
            pass
    elif page == 'Your Preferences':
        st.header('Your Preferences')
        st.write(f'Below shows the current preferences for {user_name}')
    elif page == 'Group Preferences':
        if group_name == '':
            st.warning('Group preferences will appear once you specify a group')
            st.stop()
        st.title('Group Preferences')
        st.write(f'Below shows preferences for films in the group {group_name}')


if __name__ == '__main__':
    main()