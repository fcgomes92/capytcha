from functools import wraps

from aiohttp import web
from jwt.exceptions import DecodeError
from pymodm.errors import DoesNotExist

from capytcha_server.settings import settings
from capytcha_server.utils.tokens import decode_data, encode_data
from capytcha_server.models.user import User
from capytcha_server.models.client import Client


def get_auth_header(request):
    auth_string = request.headers.get(settings.authorization_header)
    if not auth_string:
        raise ValueError('no_authorization_header')
    [scheme, token] = map(lambda v: v.strip(), auth_string.split(' '))

    if not scheme or scheme != settings.authorization_scheme:
        raise ValueError('no_authorization_scheme')

    if not token:
        raise ValueError('no_authorization_token')

    return [scheme, token]


async def check_auth_token(token, scheme=None):
    try:
        data = decode_data(token)

        email = data.get('email', None)
        if not email:
            raise ValueError('invalid_token')
        user = User.objects.get({'email': email})
        return [True, user]
    except (DecodeError, DoesNotExist):
        raise ValueError('invalid_token')


def require_authentication(f):
    @wraps(f)
    async def wrapped(request, *args, **kwargs):
        try:
            [scheme, token] = get_auth_header(request)
            [authenticated, user] = await check_auth_token(token, scheme=scheme)
            request['user'] = user
            return await f(request, *args)
        except ValueError as ve:
            return web.json_response(data={'code': str(ve)}, status=401)
    return wrapped


async def check_client_auth_token(token, scheme=None):
    try:
        data = decode_data(token)
        login = data.get('login', None)
        if not login:
            raise ValueError('invalid_token')
        client = Client.objects.get({'login': login})
        return [True, client]
    except (DecodeError, DoesNotExist):
        raise ValueError('invalid_token')


def require_client_authentication(f):
    @wraps(f)
    async def wrapped(request, *args, **kwargs):
        try:
            [scheme, token] = get_auth_header(request)
            [authenticated, client] = await check_client_auth_token(token, scheme=scheme)
            request['client'] = client
            return await f(request, *args)
        except ValueError as ve:
            return web.json_response(data={'code': str(ve)}, status=401)
    return wrapped
