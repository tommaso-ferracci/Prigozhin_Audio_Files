import pytest

from src.helper_functions import geography

def test_bakhmut():
    x, y = geography.get_coordinates("bakhmut")
    assert (round(x) == 49) and (round(y) == 38)

def test_unknown():
    x, y = geography.get_coordinates("perdindirindina")
    assert (x is None) and (y is None)  