import serpy

class ClientProfileSchema(serpy.Serializer):
    name = serpy.Field(required=False)
    login = serpy.Field(required=False)