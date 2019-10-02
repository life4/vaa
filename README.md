# VAA

VAlidators Adapter makes validation by any existing validator with the same interface.

Supported validators:

| validator | adapter |
| --------- | ------- |
| [Cerberus](http://docs.python-cerberus.org/en/stable/) | `va.cerberus` |
| [Django Forms](https://docs.djangoproject.com/en/2.2/topics/forms/) | `va.django` |
| [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) | `va.marshmallow` |
| [PySchemes](https://github.com/spy16/pyschemes) | `va.pyschemes` |
| [Django REST Framework](https://www.django-rest-framework.org/) | `va.restframework` |
| [WTForms](https://wtforms.readthedocs.io/en/stable/) | `va.wtforms` |

```bash
python3 -m pip install --user vaa
```

## Example

```python
import marshmallow
import vaa


class Scheme(marshmallow.Schema):
  id = marshmallow.fields.Int(required=True)
  name = marshmallow.fields.Str(required=True)

scheme_validator = vaa.marshmallow(Scheme)
```

## Validating data

All schemes adopted by va has the same interface:

```python
scheme = scheme_validator({'id': '1', 'name': 'Oleg'})
scheme.is_valid()  # True
scheme.cleaned_data
# {'name': 'Oleg', 'id': 1}

scheme = Scheme({'id': 'no', 'name': 'Oleg'})
scheme.is_valid()  # False
scheme.errors
# {'id': ['Not a valid integer.']}
```

If error isn't for specific field, iw will be in `__all__` key.

## Simple scheme

If you want to do validation with simple function, you can use `va.simple` adapter. For example, you want to check that in dict `{'a': ..., 'b': ...}` both values are positive. There are many ways to do so.

It can return `bool`:

```python
@vaa.simple
def validate(a, b) -> bool:
  return a > 0 and b > 0
```

Or return message for error:

```python
@vaa.simple
def validate(a, b) -> bool:
  if a > 0 and b > 0:
    return True
  return 'should be positive'
```

Or return errors dict:

```python
@vaa.simple
def validate(a, b) -> bool:
  if a <= 0:
    return {'a': 'should be positive'}
  if b <= 0:
    return {'b': 'should be positive'}
  return True
```

Or raise `va.ValidationError` with error message or dict:

```python
@vaa.simple
def validate(a, b) -> bool:
  if a > 0 and b > 0:
      return True
  raise vaa.ValidationError('should be positive')
```

Also, if you want to get the original dict without unpacking it into keyword arguments, do a function that accepts only one `_` argument:

```python
@vaa.simple
def validate(_):
  return _['a'] > 0 and _['b'] > 0
```

In that dict keys can be accessed as attributes:

```python
@vaa.simple
def validate(_):
  return _.a > 0 and _.b > 0
```

Choose the best way and follow it. Avoid mixing them in one project.
