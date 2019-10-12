from pymodm import MongoModel, fields
from pymongo import IndexModel, TEXT

from capytcha_server.models.application import Application

class Client(MongoModel):
    name = fields.CharField()
    login = fields.CharField()
    password = fields.CharField()    
    applications = fields.EmbeddedDocumentListField(Application)
    
    class Meta:
        indexes = [
            IndexModel([('login', TEXT)], unique=True)
        ]