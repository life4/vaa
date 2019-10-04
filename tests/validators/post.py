import marshmallow
import pyschemes

import vaa


class PostMarshmallow(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    mail = marshmallow.fields.Email(required=True)
    count = marshmallow.fields.Int(required=True)


post_pyschemes = pyschemes.Scheme({
    'name': str,
    'mail': str,
    'count': int,
})

postmodels = [
    PostMarshmallow,
    post_pyschemes,
]

postvalidators = [
    vaa.marshmallow(PostMarshmallow),
    vaa.pyschemes(post_pyschemes),
]
