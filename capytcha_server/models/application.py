from pymodm import MongoModel, fields

class Application(MongoModel):
    name = fields.CharField()
    tokens = fields.ListField()