'''
    File name: test_user_name_exist.py
    Author: Henry Letton
    Date created: 2021-03-25
    Python Version: 3.8.3
    Desciption: Test user_name_exist function
'''

import pytest
from src.db_fns import create_engine2, user_name_exist
import string
import random

# Function to generate a random string of acceptable characters for username
def id_generator(size = random.randrange(50)+1, 
                 chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Check that returned instance is the correct engine object
def test_for_type():
    engine = create_engine2()
    # Run 3 tests on random possible usernames
    names = [id_generator() for i in [1,2,3]]
    for user_name in names:
        message = (f'{user_name} input did not return a bool value')
        assert isinstance(user_name_exist(engine, user_name), bool), message
