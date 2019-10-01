import jwt

from capytcha_server.settings import settings


def encode_data(data) -> str:
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_data(token) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
