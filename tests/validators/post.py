import marshmallow
import pydantic
import pyschemes

import vaa


class PostMarshmallow(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    mail = marshmallow.fields.Email(required=True)
    count = marshmallow.fields.Int(required=True)


class PostPydantic(pydantic.BaseModel):
    name: str
    mail: str
    count: int


post_pyschemes = pyschemes.Scheme({
    'name': str,
    'mail': str,
    'count': int,
})

postvalidators = [
    # vaa.marshmallow(PostMarshmallow),
    vaa.pyschemes(post_pyschemes),
    vaa.pydantic(PostPydantic)
]
