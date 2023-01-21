"""Tests de una función dummy
"""
import os
import sys

from scrapper.core import sum_function_to_test

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_sum_function_to_test():
    """Test de una función dummy
    """
    assert 3 == sum_function_to_test(1,2)
