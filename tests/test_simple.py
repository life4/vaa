import pytest

import vaa


def validator_bool_kwargs(a, b):
    return a > 0 and b > 0


def validator_string_kwargs(a, b):
    if a > 0 and b > 0:
        return True
    return 'should be positive'


def validator_list_kwargs(a, b):
    if a > 0 and b > 0:
        return True
    return ['should be', 'positive']


def validator_dict_kwargs(a, b):
    if a > 0 and b > 0:
        return True
    return {'ab': ['should be positive']}


def validator_raise_kwargs(a, b):
    if a > 0 and b > 0:
        return True
    raise vaa.ValidationError('should be positive')


def validator_bool_container(_):
    return _.a > 0 and _.b > 0


def validator_string_container(_):
    if _.a > 0 and _.b > 0:
        return True
    return ['should be positive']


def validator_dict_container(_):
    if _.a > 0 and _.b > 0:
        return True
    return {'ab': ['should be positive']}


def validator_raise_container(_):
    if _.a > 0 and _.b > 0:
        return True
    raise vaa.ValidationError('should be positive')


def validator_return_error_container(_):
    if _.a > 0 and _.b > 0:
        return True
    return vaa.ValidationError('should be positive')


@pytest.mark.parametrize('validator, errors', [
    (lambda a, b: a > 0 and b > 0, [vaa.Error(message='PH')]),
    (validator_bool_kwargs, [vaa.Error(message='PH')]),
    (validator_string_kwargs, [vaa.Error(message='should be positive')]),
    (validator_list_kwargs, [vaa.Error(message='should be'), vaa.Error(message='positive')]),
    (validator_dict_kwargs, [vaa.Error(message='should be positive', field='ab')]),
    (validator_raise_kwargs, [vaa.Error(message='should be positive')]),

    (validator_bool_container, [vaa.Error(message='PH')]),
    (validator_string_container, [vaa.Error(message='should be positive')]),
    (validator_dict_container, [vaa.Error(message='should be positive', field='ab')]),
    (validator_raise_container, [vaa.Error(message='should be positive')]),
    (validator_return_error_container, [vaa.Error(message='should be positive')]),
])
def test_simple_validator(validator, errors):
    wrapped = vaa.simple(validator, error='PH')

    v = wrapped({'a': 4, 'b': 7})
    assert v.is_valid() is True
    assert v.errors is None

    v = wrapped({'a': 4, 'b': -7})
    assert v.is_valid() is False
    assert v.errors == errors
