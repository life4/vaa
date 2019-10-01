import marshmallow
import rest_framework

import va


class PostMarshmallow(marshmallow.Schema):
    id = marshmallow.fields.Int(required=True)
    name = marshmallow.fields.Str(required=True)


class PostRESTFramework(rest_framework.serializers.Serializer):
    id = rest_framework.serializers.IntegerField()
    name = rest_framework.serializers.CharField(max_length=20)


postvalidators = [
    va.marshmallow(PostMarshmallow),
    va.restframework(PostRESTFramework),
]
