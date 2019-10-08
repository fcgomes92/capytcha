from pymodm import EmbeddedMongoModel, fields
from pymongo import TEXT, IndexModel


class Application(EmbeddedMongoModel):
    name = fields.CharField()
    tokens = fields.ListField()

    @property
    def active_token(self):
        return self.tokens[0] if len(self.tokens) else None

    class Meta:
        indexes = [
            IndexModel([('login', TEXT)], unique=True)
        ]
