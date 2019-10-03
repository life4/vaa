"""Wrappers for validators

Use this classes as wrappers for non-djburger validators
"""
from typing import Dict, Any, Callable, Union, List, TypeVar, NamedTuple

from ._django_utils import safe_model_to_dict

DictStrAny = Dict[str, Any]
ErrorsDict = Dict[str, Union[List[str], DictStrAny]]

Validator = TypeVar('Validator')


class ValidationResult(NamedTuple):
    """Actual validation result which returned on every validation
    """
    cleaned_data: DictStrAny
    errors: ErrorsDict
    is_valid: bool


ValidateCallable = Callable[[DictStrAny], ValidationResult]


def django(model: Validator) -> ValidateCallable:
    """Creates validator from Django Form
    """

    def validate(data, **params) -> ValidationResult:
        m = model(data, **params)
        result = m.is_valid()
        return ValidationResult(m.cleaned_data, m.errors, result)

    return validate


def marshmallow(model: Validator) -> ValidateCallable:
    """Creates validator from Marshmallow Schema
    """
    from marshmallow import ValidationError

    def validate(data, **_) -> ValidationResult:
        cleaned_data = None
        errors = None
        try:
            cleaned_data = model().load(data)
        except ValidationError as exc:
            errors = exc.messages

        return ValidationResult(cleaned_data, errors, not errors)

    return validate


def pyschemes(scheme: Validator) -> ValidateCallable:
    """Creates validator from PySchemes scheme.
    """

    def validate(data, **_) -> ValidationResult:
        cleaned_data = None
        errors = None
        try:
            cleaned_data = scheme.validate(data)
        except Exception as e:
            errors = {'__all__': list(e.args)}
        return ValidationResult(cleaned_data, errors, not errors)

    return validate


def cerberus(model: Validator) -> ValidateCallable:
    """Creates validator from cerberus model
    """

    def validate(data, **_) -> ValidationResult:
        result = model.validate(data)
        return ValidationResult(model.document, model.errors, result)

    return validate


class DummyMultyDict(dict):
    def getlist(self, name):
        if name not in self:
            return []
        return [self[name]]


def wtforms(form: Validator) -> ValidateCallable:
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
        return ValidationResult(obj.data, obj.errors, result)

    return validate


def restframework(form: Validator) -> ValidateCallable:
    """Creates validator from Django REST Framework serializer
    """

    def validate(data, **params) -> ValidationResult:
        data = safe_model_to_dict(data)
        obj = form(data=data, **params)
        result = obj.is_valid()
        return ValidationResult(obj.validated_data, obj.errors, result)

    return validate


def _format_pydantic_exc(exc):
    errors = {}
    for e in exc.errors():
        location = errors
        *path, cause = e.pop('loc')
        for field in path:
            location = location.setdefault(field, {})
        location[cause] = e
    return errors


def pydantic(model: Validator) -> ValidateCallable:
    """Creates validator from Pydantic BaseModel
    """
    from pydantic import validate_model

    def validate(data, **_) -> ValidationResult:
        errors = None
        cleaned_data, _, exc = validate_model(model, data, raise_exc=False)
        if exc:
            errors = _format_pydantic_exc(exc)
            cleaned_data = None
        return ValidationResult(cleaned_data, errors, not errors)

    return validate
