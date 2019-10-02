"""Wrappers for validators

Use this classes as wrappers for non-djburger validators
"""
from typing import Dict, Any, Tuple, Callable, Type, Optional

from ._django_utils import safe_model_to_dict

DictStrAny = Dict[str, Any]
ValidationResult = Tuple[Optional[DictStrAny], Optional[DictStrAny], bool]
Validator = Callable[[DictStrAny], ValidationResult]


class BaseValidator:
    """
    Base class for validators
    Do not use it directly, instead use vaa.{validator_type} function to construct one
    """
    cleaned_data: DictStrAny
    errors: DictStrAny
    valid: bool

    def __init__(self, data, **kwargs):
        self.data = data
        cleaned_data, errors, is_valid = self.validator(self.data, **kwargs)
        object.__setattr__(self, 'cleaned_data', cleaned_data)
        object.__setattr__(self, 'errors', errors)
        object.__setattr__(self, 'valid', is_valid)

    def is_valid(self) -> bool:
        return self.valid

    def __setattr__(self, name, value):
        if name in ('cleaned_data', 'errors', '_is_valid'):
            raise AttributeError('Cannot set attributes cleaned_data or errors')
        object.__setattr__(self, name, value)

    @staticmethod
    def validator(data, **kwargs) -> ValidationResult:
        """This method dynamically created on wrapping a model
           It fits only one type of validator and can not be used for another
        """
        raise NotImplementedError()


ValidatorType = Type[BaseValidator]


def create_validator(model_name, validator: Validator, validator_class=BaseValidator) -> ValidatorType:
    """Dynamically creates new validator type for current model/form/schema
    """
    return type(f'{model_name}Validator', (validator_class,), dict(validator=staticmethod(validator)))


def django(model, **kwargs) -> ValidatorType:
    """Creates validator from django Form
    """
    def validate(data, **params) -> ValidationResult:
        m = model(data, **params)
        result = m.is_valid()
        return m.cleaned_data, m.errors, result

    return create_validator(model.__name__, validate, **kwargs)


def marshmallow(model, **kwargs) -> ValidatorType:
    """Creates validator from Django Form
    """
    from marshmallow import ValidationError

    def validate(data, **_) -> ValidationResult:
        cleaned_data = None
        errors = None
        try:
            cleaned_data = model().load(data)
        except ValidationError as exc:
            errors = exc.messages

        return cleaned_data, errors, not errors

    return create_validator(model.__name__, validate, **kwargs)


def pyschemes(scheme, **kwargs) -> ValidatorType:
    """Creates validator from PySchemes scheme.
    """
    def validate(data, **_) -> ValidationResult:
        cleaned_data = None
        errors = None
        try:
            cleaned_data = scheme.validate(data)
        except Exception as e:
            errors = {'__all__': list(e.args)}
        return cleaned_data, errors, not errors

    return create_validator(type(scheme).__name__, validate, **kwargs)


def cerberus(model, **kwargs) -> ValidatorType:
    """Creates validator from cerberus model
    """
    def validate(data, **_) -> ValidationResult:
        result = model.validate(data)
        return model.document, model.errors, result

    return create_validator(type(model).__name__, validate, **kwargs)


class DummyMultyDict(dict):
    def getlist(self, name):
        if name not in self:
            return []
        return [self[name]]


def wtforms(form, **kwargs) -> ValidatorType:
    """Creates validator from WTForm
    """
    def validate(data, **params) -> ValidationResult:
        # if MultiDict passed
        if hasattr(data, 'getlist'):
            obj = form(data, **params)
        else:
            data = safe_model_to_dict(data)
            obj = form(DummyMultyDict(data), **params)
        result = obj.validate()
        return obj.data, obj.errors, result

    return create_validator(form.__name__, validate, **kwargs)


def restframework(form, **kwargs) -> ValidatorType:
    """Creates validator from Django REST Framework serializer
    """
    def validate(data, **params) -> ValidationResult:
        data = safe_model_to_dict(data)
        obj = form(data=data, **params)
        result = obj.is_valid()
        return obj.validated_data, obj.errors, result

    return create_validator(form.__name__, validate, **kwargs)


def _format_pydantic_exc(exc):
    errors = {}
    for e in exc.errors():
        location = errors
        *path, cause = e.pop('loc')
        for field in path:
            location = location.setdefault(field, {})
        location[cause] = e
    return errors


def pydantic(model, **kwargs) -> ValidatorType:
    """Creates validator from Pydantic BaseModel
    """
    from pydantic import validate_model

    def validate(data, **_) -> ValidationResult:
        errors = None
        cleaned_data, _, exc = validate_model(model, data, raise_exc=False)
        if exc:
            errors = _format_pydantic_exc(exc)
            cleaned_data = None
        return cleaned_data, errors, not errors

    return create_validator(model.__name__, validate, **kwargs)
