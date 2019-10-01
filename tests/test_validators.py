import pytest

from .validators.pre import prevalidators
from .validators.post import postvalidators


validators = prevalidators + postvalidators


@pytest.mark.parametrize('validator', validators)
def test_valid(validator):
    data = {
        'name': 'Max',
        'mail': 'test@example.ru',
        'count': 20,
    }
    v = validator(data=data)
    assert v.is_valid() is True
    assert v.cleaned_data == data


@pytest.mark.parametrize('validator', validators)
def test_no_field(validator):
    data = {
        'name': 'Max',
        'mail': 'test@example.ru',
    }
    v = validator(data=data)
    assert v.is_valid() is False
    assert v.errors


@pytest.mark.parametrize('validator', validators)
def test_invalid_int(validator):
    data = {
        'name': 'Max',
        'mail': 'test@example.ru',
        'count': 'lol',
    }
    v = validator(data=data)
    assert v.is_valid() is False
    assert v.errors
