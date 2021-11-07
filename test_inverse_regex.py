

import pytest
from inverse_regex import inverse_regex
import numpy as np
import pandas as pd


def test_invalid_types():
    with pytest.raises(TypeError):
        inverse_regex(None)
    with pytest.raises(TypeError):
        inverse_regex(range(1))
    with pytest.raises(TypeError):
        inverse_regex({'a': 1})
    with pytest.raises(TypeError):
        inverse_regex({1, 2})
    with pytest.raises(TypeError):
        inverse_regex(b"a")
    with pytest.raises(TypeError):
        inverse_regex(bytearray(1))
                
def test_basic_strings():
    assert inverse_regex('A') == '[[:upper:]]'
    assert inverse_regex('a') == '[[:lower:]]'
    assert inverse_regex('1') == '[[:digit:]]'
    assert inverse_regex('aA1') == '[[:lower:]][[:upper:]][[:digit:]]'
    assert inverse_regex('~!@#$%^&*()_+}{|":?><,./;[]-=') == '~!@#$%^&*()_+}{|":?><,./;[]-='
    assert inverse_regex('\\') == '\\'
    assert inverse_regex(' \t\n\r') == ' \t\n\r'
    assert inverse_regex('a', enclose = True) == '^[[:lower:]]$'

def test_combine_cases():
    assert inverse_regex('A', combine_cases = True) == '[[:alpha:]]'
    assert inverse_regex('a', combine_cases = True) == '[[:alpha:]]'
    assert inverse_regex('Aa', combine_cases = True) == '[[:alpha:]]{2}'

def test_combine_alphanumeric():
    assert inverse_regex('A', combine_alphanumeric = True) == '[[:alnum:]]'
    assert inverse_regex('a', combine_alphanumeric = True) == '[[:alnum:]]'
    assert inverse_regex('a1', combine_alphanumeric = True) == '[[:alnum:]]{2}'

def test_combine_punctuation():
    assert inverse_regex('~!@#$%^&*()_+}{|":?><,./;[]-=', combine_punctuation = True, numbers_to_keep = 29) == '[[:punct:]]{29}'
    assert inverse_regex('\\', combine_punctuation = True) == '[[:punct:]]'

def test_combine_space():
    assert inverse_regex(' \t\n\r', combine_space = True) == '[[:space:]]{4}'

def test_numbers_to_keep():
    assert inverse_regex('1', numbers_to_keep = None) == '[[:digit:]]'
    assert inverse_regex('1', numbers_to_keep = ()) == '[[:digit:]]'
    assert inverse_regex('1', numbers_to_keep = 1) == '[[:digit:]]{1}'
    assert inverse_regex('12', numbers_to_keep = 2) == '[[:digit:]]{2}'
    assert inverse_regex('12', numbers_to_keep = 1) == '[[:digit:]]+'
    assert inverse_regex('12345', numbers_to_keep = (1,2,3,4,5,)) == '[[:digit:]]{5}'
    assert inverse_regex('12345', numbers_to_keep = (10,)) == '[[:digit:]]+'
    assert inverse_regex(55 * '1', numbers_to_keep = tuple([n for n in range(10, 100)])) == '[[:digit:]]{55}'

def test_escape():
    assert inverse_regex('~!@#$%^&*()_+}{|":?><,./;[]-=') == '~!@#$%^&*()_+}{|":?><,./;[]-='
    assert inverse_regex('~!@#$%^&*()_+}{|":?><,./;[]-=', escape = True) == '\\~!@\\#\\$%\\^\\&\\*\\(\\)_\\+\\}\\{\\|":\\?><,\\./;\\[\\]\\-='

    assert inverse_regex('\\') == '\\'
    assert inverse_regex('\\', escape = True) == '\\\\'

def test_bool():
    pass ## TODO

def test_int():
    pass ## TODO

def test_float():
    pass ## TODO

def test_complex():
    pass ## TODO

def test_tuple():
    pass ## TODO

def test_list():
    pass ## TODO

def test_numpy():
    pass ## TODO

def test_pandas():
    pass ## TODO





