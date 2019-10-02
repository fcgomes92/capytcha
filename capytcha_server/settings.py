import os

from capytcha_server.utils.singleton import Singleton
from pymodm.connection import connect


class Constants:
    APP_NAME = 'APP_NAME'

    JWT_SECRET = 'JWT_SECRET'
    JWT_ALGORITHM = 'JWT_ALGORITHM'

    IMAGE_STORAGE = 'IMAGE_STORAGE'
    IMAGE_STORAGE_LOCAL = 'LOCAL'
    IMAGE_STORAGE_S3 = 'S3'

    IMAGE_STORAGE_PATH = 'IMAGE_STORAGE_PATH'

    DB_CON = 'DB_CON'


class Settings(Singleton):
    jwt_secret = None

    def configure_db(self):
        self.db_con = os.environ.get(Constants.DB_CON)
        self.database = connect(self.db_con, alias=self.app_name)

    def parse_storage_path(self):
        path = os.environ.get(Constants.IMAGE_STORAGE_PATH)
        self.image_storage_path = os.path.abspath(path)

    def __init__(self, *args, **kwargs):
        self.app_name = os.environ.get(Constants.APP_NAME)
        self.jwt_secret = os.environ.get(Constants.JWT_SECRET)
        self.jwt_algorithm = os.environ.get(Constants.JWT_ALGORITHM)

        self.image_storage = os.environ.get(Constants.IMAGE_STORAGE)
        if (self.image_storage == Constants.IMAGE_STORAGE_LOCAL):
            self.parse_storage_path()


settings = Settings()
