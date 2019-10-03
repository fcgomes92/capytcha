from datetime import datetime

from pymodm import MongoModel, fields

from capytcha_server.models.application import Application
from capytcha_server.settings import settings


class LogCodes:
    DELETE = 'delete'
    CREATE_USER = 'create_user'


availableLogCodes = list(map(lambda v: v.lower(), filter(
    lambda v: v and not v.startswith('_'), LogCodes.__dict__.keys())))


class Log(MongoModel):
    created = fields.DateTimeField(
        default=lambda: datetime.utcnow().strftime(settings.server_date_format))
    code = fields.CharField(choices=availableLogCodes)
    message = fields.DictField()
