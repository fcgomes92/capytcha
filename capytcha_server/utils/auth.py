from functools import wraps

from aiohttp import web
from jwt.exceptions import DecodeError
from pymodm.errors import DoesNotExist

from capytcha_server.models.client import Client
from capytcha_server.models.user import User
from capytcha_server.settings import settings
from capytcha_server.utils.tokens import decode_data, encode_data


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


async def check_auth_token(token, scheme=None, model=User, field='email'):
    try:
        data = decode_data(token)

        auth_reference = data.get(field, None)
        if not auth_reference:
            raise ValueError('invalid_token')
        user = model.objects.get({field: auth_reference})
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


def require_client_authentication(f):
    @wraps(f)
    async def wrapped(request, *args, **kwargs):
        try:
            [scheme, token] = get_auth_header(request)
            [authenticated, user] = await check_auth_token(token, model=Client, field='login')
            request['user'] = user
            return await f(request, *args)
        except ValueError as ve:
            return web.json_response(data={'code': str(ve)}, status=401)
    return wrapped
