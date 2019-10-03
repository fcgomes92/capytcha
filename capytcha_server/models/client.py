from pymodm import MongoModel, fields
from capytcha_server.models.application import Application

class Client(MongoModel):
    name = fields.CharField()
    applications = fields.EmbeddedDocumentListField(Application)
