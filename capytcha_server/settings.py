import os

from capytcha_server.utils.singleton import Singleton
from pymodm.connection import connect
from capytcha_server.models.user import User


class Constants:
    APP_NAME = 'APP_NAME'

    JWT_SECRET = 'JWT_SECRET'
    JWT_ALGORITHM = 'JWT_ALGORITHM'

    IMAGE_STORAGE = 'IMAGE_STORAGE'
    IMAGE_STORAGE_LOCAL = 'LOCAL'
    IMAGE_STORAGE_S3 = 'S3'
    IMAGE_STORAGE_PATH = 'IMAGE_STORAGE_PATH'

    MONGODB_URI = 'MONGODB_URI'


class Settings(Singleton):
    jwt_secret = None

    def configure_db(self):
        self.mongodb_uri = os.environ.get(Constants.MONGODB_URI)
        connect(self.mongodb_uri)

    def parse_storage_path(self):
        path = os.environ.get(Constants.IMAGE_STORAGE_PATH)
        self.image_storage_path = os.path.abspath(path)

    def __init__(self, *args, **kwargs):
        self.app_name = os.environ.get(Constants.APP_NAME)
        self.jwt_secret = os.environ.get(Constants.JWT_SECRET)
        self.jwt_algorithm = os.environ.get(Constants.JWT_ALGORITHM)

        self.server_date_format = '%Y-%m-%d %H:%M:%S'

        self.image_storage = os.environ.get(Constants.IMAGE_STORAGE)
        if (self.image_storage == Constants.IMAGE_STORAGE_LOCAL):
            self.parse_storage_path()

        self.configure_db()


settings = Settings()
