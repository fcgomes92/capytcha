from aiohttp import web

from capytcha_server.utils.auth import require_authentication
from capytcha_server.schemas.client import ClientProfileSchema

client_routes = web.RouteTableDef()


@client_routes.get('/clients/me')
@require_authentication
async def get_client_data(request: web.Request) -> web.Response:
    return web.json_response(data=ClientProfileSchema(request['user']).data)
