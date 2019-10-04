import cerberus
import wtforms

import vaa


class PreWTForms(wtforms.Form):
    name = wtforms.StringField('Name', [
        wtforms.validators.DataRequired(),
    ])
    mail = wtforms.StringField('E-Mail', [
        wtforms.validators.DataRequired(), wtforms.validators.Email(),
    ])
    count = wtforms.IntegerField('Count', [
        wtforms.validators.DataRequired(), wtforms.validators.NumberRange(min=0),
    ])


scheme = dict(
    name=dict(
        type='string',
        required=True,
    ),
    mail=dict(
        type='string',
        required=True,
        # http://docs.python-cerberus.org/en/stable/validation-rules.html#regex
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    ),
    count=dict(
        type='integer',
        required=True,
        coerce=int,
    ),
)
PreCerberus = cerberus.Validator(scheme, purge_unknown=True)


premodels = [
    PreWTForms,
    PreCerberus,
]

prevalidators = [
    vaa.wtforms(PreWTForms),
    vaa.cerberus(PreCerberus),
]
