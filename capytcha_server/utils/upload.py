import os
from functools import wraps
from uuid import uuid4

from capytcha_server.settings import Constants, settings


def _download_local():
    pass


def _upload_local(token, image, audio):
    image_audio_id = str(uuid4())
    path = os.path.join(settings.image_storage_path,f'{image_audio_id}')
    image.save(f'{path}.png', 'png')
    with open(f'{path}.wav', 'wb') as f:
        f.write(audio)
    return image_audio_id


def _download_s3():
    pass


def _upload_s3():
    pass


def _check_storage_mode(action):
    def inner_function(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            functions = []
            if settings.image_storage == Constants.IMAGE_STORAGE_LOCAL:
                functions = [_download_local, _upload_local]
            elif settings.image_storage == Constants.IMAGE_STORAGE_S3:
                functions = [_download_s3, _upload_s3]
            return functions[0](*args, **kwargs) if action == 'download' else functions[1](*args, **kwargs)
        return wrapped
    return inner_function


@_check_storage_mode('download')
def download_captcha(token):
    pass


@_check_storage_mode('upload')
def upload_captcha(token, image, audio):
    pass
