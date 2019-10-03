import importlib
import logging

from . import _external

logger = logging.getLogger('vaa')

SUPPORTED_VALIDATORS = {
    'cerberus.Validator': _external.Cerberus,
    'django.forms.Form': _external.Django,
    'marshmallow.Schema': _external.Marshmallow,
    'pyschemes.Scheme': _external.PySchemes,
    'rest_framework.serializers.Serializer': _external.RESTFramework,
    'wtforms.Form': _external.WTForms,
}


def get_from(validator):
    for v, wrapper in available_validators.items():
        if isinstance(validator, v) or (isinstance(validator, type) and issubclass(validator, v)):
            return wrapper(validator)
    raise TypeError(f'No wrapper found for {validator}.')


def _get_available_validators():
    for validator, wrapper in SUPPORTED_VALIDATORS.items():
        try:
            module, validator = validator.rsplit('.', 1)
            module = importlib.import_module(module)
            available_validators[getattr(module, validator)] = wrapper
        except ImportError:
            pass
    logger.debug(f'Found {len(available_validators)} validators: {list(available_validators)}')


if 'available_validators' not in globals():
    available_validators = {}
    _get_available_validators()
