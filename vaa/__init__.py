"""Validators Adapter. The common interface for all validators.
"""


from ._aliases import (
    simple,
)
from ._external import (
    wtforms,
    restframework,
    pydantic,
    pyschemes,
    marshmallow,
    django,
    cerberus,
)
from ._internal import ValidationError


__version__ = '0.1.4'

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
