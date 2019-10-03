import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from random import randrange

from aiohttp import web

from capytcha.capytcha import (create_audio_captcha, create_image_captcha,
                               create_random_number, create_random_text)
from capytcha_server.exceptions import (AioHttpAppException,
                                        GracefulExitException, ResetException)
from capytcha_server.routes.captcha import captcha_routes
from capytcha_server.routes.public import public_routes
from capytcha_server.utils.handlers import (cancel_tasks, handle_sighup,
                                            handle_sigterm)
from capytcha_server.utils.tokens import decode_data, encode_data
from capytcha_server.utils.upload import download_captcha, upload_captcha

HOSTNAME: str = os.environ.get("HOSTNAME", "Unknown")


def assign_routes(app):
    app.router.add_routes(captcha_routes)
    app.router.add_routes(public_routes)
    return app


async def create_app():
    """Run the application
    Return whether the application should restart or not.
    """
    app = web.Application()
    assign_routes(app)

    return app


def run_app() -> bool:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    app = web.Application()
    assign_routes(app)

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
