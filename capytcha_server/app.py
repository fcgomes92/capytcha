import asyncio
import logging
import os
import signal
import sys
from concurrent.futures import CancelledError
from datetime import datetime
from random import randrange

from aiohttp import web
from aiohttp.abc import AbstractAccessLogger

from capytcha.capytcha import (create_audio_captcha, create_image_captcha,
                               create_random_number, create_random_text)
from capytcha_server.exceptions import (AioHttpAppException,
                                        GracefulExitException, ResetException)
from capytcha_server.utils.tokens import decode_data, encode_data
from capytcha_server.utils.upload import download_captcha, upload_captcha

HOSTNAME: str = os.environ.get("HOSTNAME", "Unknown")

routes = web.RouteTableDef()


class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        self.logger.info(f'{request.remote} '
                         f'"{request.method} {request.path} '
                         f'done in {time}s: {response.status}')


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    timestamp = datetime.now().isoformat()
    return web.json_response(data={})


@routes.get('/health')
async def health(request: web.Request) -> web.Response:
    return web.json_response(data={'data': 'HEALTHY'})

# TODO: add auth
@routes.post('/captcha/get')
async def get_captcha(request: web.Request) -> web.Response:
    """ 
    get a new image + sound + token
    """
    captcha_text = create_random_text()
    captcha_audio = create_random_number()

    image = create_image_captcha(captcha_text)
    audio = create_audio_captcha(captcha_audio)

    # saves to the fs
    resource_id = upload_captcha(image, audio)
    # saves to the database
    # TODO: save to the database

    token = encode_data({'id': '<user_id>', 'resource': resource_id}).decode()

    return web.json_response(data={
        'token': token,
    })

# TODO: add auth
@routes.post('/captcha/check')
async def get_captcha(request: web.Request) -> web.Response:
    """
    body: {
        "token": "<JWT Token>",
        "image": "<user input response based on the image provided>",
        "audio": "<user input response based on the audio provided>"
    }
    """
    # TODO: add body validation
    data = type('', (), await request.json())
    token_data = decode_data(data.token)
    # TODO:
    #   get from the database based on the resource (token_data)
    #   get the audio and image values and compare then
    #   return if one or both are correct
    return web.json_response(data={}, status=400)


def handle_sighup() -> None:
    logging.warning("Received SIGHUP")
    raise ResetException("Application reset requested via SIGHUP")


def handle_sigterm() -> None:
    logging.warning("Received SIGTERM")
    raise ResetException("Application exit requested via SIGTERM")


def cancel_tasks() -> None:
    for task in asyncio.Task.all_tasks():
        task.cancel()

# TODO: add auth


async def create_app():
    """Run the application
    Return whether the application should restart or not.
    """
    app = web.Application()
    app.router.add_routes(routes)

    return app


def run_app() -> bool:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    app = web.Application()
    app.router.add_routes(routes)

    try:
        web.run_app(app, handle_signals=True,
                    access_log_format='%a %t "%r" %s %b :: %T	')
    except ResetException:
        logging.warning("Reloading...")
        cancel_tasks()
        asyncio.set_event_loop(asyncio.new_event_loop())
        return True
    except GracefulExitException:
        logging.warning("Exiting...")
        cancel_tasks()
        loop.close()

    return False


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    """The main loop."""
    while run_app():
        pass


if __name__ == "__main__":
    main()
