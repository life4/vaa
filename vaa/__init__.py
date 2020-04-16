"""Validators Adapter. The common interface for all validators.
"""


from ._aliases import (
    cerberus,
    django,
    marshmallow,
    pyschemes,
    simple,
    restframework,
    wtforms,
)
from ._auto import validators
from ._internal import ValidationError


__version__ = '0.2.0'

__all__ = [
    'cerberus',
    'django',
    'get_from',
    'marshmallow',
    'pyschemes',
    'restframework',
    'simple',
    'ValidationError',
    'wtforms',
]


wrap = validators.wrap
