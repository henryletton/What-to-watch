'''
    File name: test_add_one.py
    Author: Henry Letton
    Date created: 2020-10-30
    Python Version: 3.8.3
    Desciption: Test the add_one function
'''

import pytest
from simple_functions import add_one

def test_for_int():
    assert isinstance(add_one(1), int)
    assert add_one(1) == 2, "One plus one is not two!"
    # Check it errors with a string
    with pytest.raises(TypeError):
        add_one("1")

def test_for_float():
    actual = add_one(1.5)
    expected = 2.5
    message = (f"add_one(1.5) returned {actual} instead of {expected}")
    assert actual == pytest.approx(expected), message
    
    