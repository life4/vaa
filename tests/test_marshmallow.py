import marshmallow
import vaa


@vaa.marshmallow
class Scheme(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    mail = marshmallow.fields.Email(required=True)
    count = marshmallow.fields.Int(required=True)


def test_valid():
    data = {'name': 'Gram', 'mail': 'master_fess@mail.ru', 'count': 10}
    v = Scheme(data)
    assert v.is_valid() is True
    assert v.cleaned_data == data
    assert v.errors is None


def test_invalid_name():
    data = {'name': 'Gram', 'mail': 'mail.ru', 'count': 10}
    v = Scheme(data)
    assert v.is_valid() is False
    assert v.cleaned_data is None
    assert v.errors == {'mail': ['Not a valid email address.']}
