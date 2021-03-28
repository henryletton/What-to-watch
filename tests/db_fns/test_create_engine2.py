'''
    File name: test_create_engine2.py
    Author: Henry Letton
    Date created: 2021-03-25
    Python Version: 3.8.3
    Desciption: Test create_engine2 function
'''

import pytest
from src.db_fns import create_engine2
import sqlalchemy
import os

# Check that returned instance is the correct engine object
def test_for_type():
    engine = create_engine2()
    message = ('Returned object is not an instance of sqlalchemy.engine.base.Engine')
    assert isinstance(engine, sqlalchemy.engine.base.Engine), message

# Confrim that enviroment variables required for db engine exists
def test_env_vars():
    # Variable to update after checking for env vars
    missing_var_count = 0
    message = ''
    
    # Check if each var exists
    for var in ['sql_user', 'sql_pw', 'sql_db']:
        if os.environ.get(var) is None:
            missing_var_count += 1
            message += f'{var} is missing from env\n'
    # If missing_var_count>0 then there is an issue, and message has content to print
    assert missing_var_count == 0, message
