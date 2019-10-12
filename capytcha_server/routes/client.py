from aiohttp import web
from pymongo.errors import DuplicateKeyError

from capytcha_server.models.client import Client
from capytcha_server.schemas.client import ClientProfileSchema
from capytcha_server.utils.auth import (require_authentication,
                                        require_client_authentication)

client_routes = web.RouteTableDef()


@client_routes.get('/clients/me')
@require_client_authentication
async def get_client_data(request: web.Request) -> web.Response:
    return web.json_response(data=ClientProfileSchema(request['user']).data)


@client_routes.post('/clients')
@require_authentication
async def create_client(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        client = Client(**data).save()
    except DuplicateKeyError as e:
        return web.json_response(data={'code': 'client_already_exists'}, status=409)
    return web.json_response(data={})
