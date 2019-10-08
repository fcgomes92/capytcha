import serpy

from capytcha_server.schemas.application import ClientApplicationSchema


class ClientProfileSchema(serpy.Serializer):
    name = serpy.Field(required=False)
    login = serpy.Field(required=False)
    applications = ClientApplicationSchema(many=True)
