import serpy

from capytcha_server.models.application import Application


class ClientApplicationSchema(serpy.Serializer):
    name = serpy.Field(required=False)
    token = serpy.Field(attr='active_token')
