import serpy

from capytcha_server.schemas.application import ApplicationSchema


class ClientProfileSchema(serpy.Serializer):
    name = serpy.Field(required=False)
    login = serpy.Field(required=False)
    applications = ApplicationSchema(many=True)
