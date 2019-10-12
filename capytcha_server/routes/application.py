from datetime import datetime
from aiohttp import web

from capytcha_server.models.application import Application
from capytcha_server.models.client import Client
from capytcha_server.utils.auth import (require_authentication,
                                        require_client_authentication)
from capytcha_server.utils.logger import logger
from capytcha_server.utils.tokens import encode_data
from capytcha_server.schemas.application import ApplicationSchema

application_routes = web.RouteTableDef()


@application_routes.get('/applications')
@require_client_authentication
async def get_client_data(request: web.Request) -> web.Response:
    schema = ApplicationSchema(request['user'].applications, many=True)
    return web.json_response(data=schema.data)


@application_routes.post('/applications')
@require_client_authentication
async def create_client(request: web.Request) -> web.Response:
    data = await request.json()
    client = request['user']
    try:
        data['tokens'] = [encode_data({'id_client': str(client._id), 'created_at': datetime.now().isoformat()}).decode()]
        app = Application(**data)
        client.applications = [app, *client.applications]
        client.save()
    except Exception as e:
        logger.error(e)
        return web.json_response(data={}, status=400)
    else:
        schema = ApplicationSchema(app)    
        return web.json_response(data=schema.data)
