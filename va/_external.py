"""Wrappers for validators

Use this classes as wrappers for non-djburger validators
"""

from ._django_utils import safe_model_to_dict


class _BaseWrapper:

    def __init__(self, validator):
        self.validator = validator

    def __call__(self, data, **kwargs):
        obj = self.validator(**kwargs)
        obj.data = safe_model_to_dict(data)
        # bound method to obj
        obj.is_valid = self.is_valid.__get__(obj)
        return obj


class Django(_BaseWrapper):
    """Wrapper for use Django Form (or ModelForm) as validator.
    """

    def __call__(self, **kwargs):
        obj = self.validator(**kwargs)
        return obj


class Marshmallow(_BaseWrapper):
    """Wrapper for use marshmallow scheme as validator.
    """

    # method binded to wrapped walidator
    @staticmethod
    def is_valid(self) -> bool:
        self.cleaned_data, self.errors = self.load(self.data)
        return not self.errors


class PySchemes(_BaseWrapper):
    """Wrapper for use PySchemes as validator.
    """

    def __call__(self, data, **kwargs):
        self.data = data
        return self

    def is_valid(self) -> bool:
        self.cleaned_data = None
        self.errors = None
        try:
            self.cleaned_data = self.validator.validate(self.data)
        except Exception as e:
            self.errors = {'__all__': list(e.args)}
            return False
        return True


class Cerberus(_BaseWrapper):
    """Wrapper for use Cerberus as validator.
    """

    def __call__(self, data, **kwargs):
        self.data = data
        return self

    def is_valid(self) -> bool:
        result = self.validator.validate(self.data)
        self.cleaned_data = self.validator.document
        self.errors = self.validator.errors
        return result


class DummyMultyDict(dict):
    def getlist(self, name):
        if name not in self:
            return []
        return [self[name]]


class WTForms(_BaseWrapper):
    """Wrapper for use WTForms form as validator.
    """

    def __call__(self, data, **kwargs):
        # if MultiDict passed
        if hasattr(data, 'getlist'):
            obj = self.validator(data, **kwargs)
        else:
            data = safe_model_to_dict(data)
            obj = self.validator(DummyMultyDict(data), **kwargs)

        # bound methods to obj
        obj.is_valid = obj.validate
        obj.cleaned_data = self.cleaned_data.__get__(obj)
        return obj

    # should be static to be not attached to the current class
    @staticmethod
    @property
    def cleaned_data(self):
        return self.data


class RESTFramework(_BaseWrapper):
    """Wrapper for use Django REST Framework serializer as validator.
    """

    def __call__(self, data, **kwargs):
        data = safe_model_to_dict(data)
        obj = self.validator(data=data, **kwargs)
        # bound method to obj
        obj.is_valid = self.is_valid.__get__(obj)
        return obj

    # method binded to wrapped validator
    @staticmethod
    def is_valid(self) -> bool:
        result = super(self.__class__, self).is_valid()
        self.cleaned_data = self.validated_data
        return result
