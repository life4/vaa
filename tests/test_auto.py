import pytest

import vaa
from .validators.post import postmodels
from .validators.pre import premodels

models = postmodels + premodels


@pytest.mark.parametrize('model', models)
def test_auto(model):
    data = {
        'name': 'Oleg',
        'mail': 'test@example.ru',
        'count': 20,
    }
    validator = vaa.get_from(model)
    v = validator(data=data)
    assert v.is_valid() is True
    assert v.cleaned_data == data


def test_wrong_model():
    with pytest.raises(TypeError, match="No wrapper found for <class 'object'>."):
        vaa.get_from(object)
