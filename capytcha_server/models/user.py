from pymodm import MongoModel, fields
from pymongo import IndexModel, TEXT


class User(MongoModel):
    email = fields.EmailField()
    first_name = fields.CharField()
    last_name = fields.CharField()
    password = fields.CharField()

    class Meta:
        indexes = [
            IndexModel([('email', TEXT)], unique=True)
        ]
