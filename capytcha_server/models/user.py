from pymodm import MongoModel, fields

class User(MongoModel):
    email = fields.EmailField()
    first_name = fields.CharField()
    last_name = fields.CharField()