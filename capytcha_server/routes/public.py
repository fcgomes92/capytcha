from datetime import datetime

from aiohttp import web

public_routes = web.RouteTableDef()


@public_routes.get('/')
async def hello(request: web.Request) -> web.Response:
    timestamp = datetime.now().isoformat()
    return web.json_response(data={})


@public_routes.get('/health')
async def health(request: web.Request) -> web.Response:
    return web.json_response(data={'data': 'HEALTHY'})
