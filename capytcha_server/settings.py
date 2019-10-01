import os

from dotenv import load_dotenv

from capytcha_server.utils.singleton import Singleton


class Constants:
    JWT_SECRET = 'JWT_SECRET'
    JWT_ALGORITHM = 'JWT_ALGORITHM'

    IMAGE_STORAGE = 'IMAGE_STORAGE'
    IMAGE_STORAGE_LOCAL = 'LOCAL'
    IMAGE_STORAGE_S3 = 'S3'

    IMAGE_STORAGE_PATH = 'IMAGE_STORAGE_PATH'


class Settings(Singleton):
    jwt_secret = None

    def parse_storage_path(self):
        path = os.environ.get(Constants.IMAGE_STORAGE_PATH)
        self.image_storage_path = os.path.abspath(path)

    def __init__(self, *args, **kwargs):
        load_dotenv()

        self.jwt_secret = os.environ.get(Constants.JWT_SECRET)
        self.jwt_algorithm = os.environ.get(Constants.JWT_ALGORITHM)

        self.image_storage = os.environ.get(Constants.IMAGE_STORAGE)
        if (self.image_storage == Constants.IMAGE_STORAGE_LOCAL):
            self.parse_storage_path()


settings = Settings()
