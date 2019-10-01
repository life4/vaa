import pytest

from .validators.pre import prevalidators
from .validators.post import postvalidators


validators = prevalidators + postvalidators


@pytest.mark.parametrize('validator', validators)
def test_valid(validator):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
        'count': 20,
    }
    v = validator(data=data)
    assert v.is_valid() is True
    assert v.cleaned_data == data


@pytest.mark.parametrize('validator', validators)
def test_no_field(validator):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
    }
    v = validator(data=data)
    assert v.is_valid() is False
    assert v.errors


@pytest.mark.parametrize('validator', validators)
def test_invalid_int(validator):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
        'count': 'lol',
    }
    v = validator(data=data)
    assert v.is_valid() is False
    assert v.errors


@pytest.mark.parametrize('validator', prevalidators)
def test_types_converting(validator):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
        'count': '10',
    }
    v = validator(request=True, data=data)
    assert v.is_valid() is True
    assert not v.errors
    assert 'count' in v.cleaned_data
    assert v.cleaned_data['count'] == 10


@pytest.mark.parametrize('validator', prevalidators)
def test_explicit_keys(validator):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
        'count': 10,
        'junk': 'test',
    }
    v = validator(request=True, data=data)
    assert v.is_valid() is True
    assert not v.errors
    assert 'junk' not in v.cleaned_data
