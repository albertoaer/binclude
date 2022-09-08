from .utils import valid_name

def test_valid_name():
    assert valid_name('a12B')
    assert valid_name('OOoe1')
    assert not valid_name('8eo')
    assert not valid_name('')
    assert valid_name('a')
    assert not valid_name('5')
    assert not valid_name('?')
    assert not valid_name('.')
    assert not valid_name('a?')
    assert not valid_name('e.')
    assert not valid_name('test.py')
    assert valid_name('test')