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
from ._internal import ValidationError


__version__ = '0.1.2'

__all__ = [
    'cerberus',
    'django',
    'marshmallow',
    'pyschemes',
    'restframework',
    'simple',
    'ValidationError',
    'wtforms',
]
