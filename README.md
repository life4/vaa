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

@vaa.marshmallow
class Scheme(marshmallow.Schema):
  id = marshmallow.fields.Int(required=True)
  name = marshmallow.fields.Str(required=True)
```

## Validating data

All schemes adopted by vaa has the same interface:

```python
validator = Scheme({'id': '1', 'name': 'Oleg'})
validator.is_valid()    # True
validator.cleaned_data  # {'name': 'Oleg', 'id': 1}

validator = Scheme({'id': 'no', 'name': 'Oleg'})
validator.is_valid()    # False
validator.errors        # [Error(message='Not a valid integer.', field='id')]
```

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

## Unknown scheme

If you're making a library that should accept any validator without explicit vaa usage, use `vaa.wrap`:

```python
class Scheme(marshmallow.Schema):
  id = marshmallow.fields.Int(required=True)
  name = marshmallow.fields.Str(required=True)

validator = vaa.wrap(Scheme)({'id': 'no', 'name': 'Oleg'})
validator = Scheme({'id': 'no', 'name': 'Oleg'})
validator.is_valid()    # False
validator.errors        # [Error(message='Not a valid integer.', field='id')]
```
