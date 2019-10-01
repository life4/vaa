import inspect

from ._django_utils import safe_model_to_dict
from ._interface import IValidator


class ValidationError(ValueError):
    pass


class Simple(IValidator):

    def __init__(self, validator, error='validation error', param='_'):
        params = inspect.signature(validator).parameters.keys()
        if tuple(params) == (param,):
            self.validator = validator
        else:
            self.validator = lambda _: validator(**_)

        self.validator = validator
        self.error = error

    def __call__(self, data, **kwargs):
        self.data = safe_model_to_dict(data)
        self.kwargs = kwargs
        return self

    def is_valid(self) -> bool:
        self.cleaned_data = None
        self.errors = None

        try:
            result = self.validator(self.data, **self.kwargs)
        except ValidationError as exc:
            result = exc.args[0]

        # returned something falsy
        if not result:
            self.errors = {'__all__': self.error}
            return False

        # returned error message
        if type(result) is str:
            self.errors = {'__all__': result}
            return False

        # returned dict of errors
        if type(result) is dict:
            self.errors = result
            return False

        # returned something truely
        self.cleaned_data = self.data
        return True
