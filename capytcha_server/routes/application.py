from aiohttp import web

from capytcha_server.models.application import Application
from capytcha_server.models.client import Client
from capytcha_server.utils.auth import (require_authentication,
                                        require_client_authentication)

application_routes = web.RouteTableDef()


@application_routes.get('/applications')
@require_client_authentication
async def get_client_data(request: web.Request) -> web.Response:
    return web.json_response(data={})


@application_routes.post('/applications')
@require_client_authentication
async def create_client(request: web.Request) -> web.Response:
    data = await request.json()
    client = request['user']
    app = Application(**data)
    client.applications = [app, *client.applications]
    client.save()
    return web.json_response(data={})
