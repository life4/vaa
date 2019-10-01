import marshmallow
import pyschemes

import va


class PostMarshmallow(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    mail = marshmallow.fields.Email(required=True)
    count = marshmallow.fields.Int(required=True)


post_pyschemes = pyschemes.Scheme({
    'name': str,
    'mail': str,
    'count': int,
})

postvalidators = [
    # va.marshmallow(PostMarshmallow),
    va.pyschemes(post_pyschemes),
]
