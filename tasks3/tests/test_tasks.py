from tasks3 import inc

def test_inc_positive():
    assert inc(5) == 6

def test_inc_zero():
    assert inc(0) == 1
