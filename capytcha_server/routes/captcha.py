from aiohttp import web

from capytcha.capytcha import (create_audio_captcha, create_image_captcha,
                               create_random_number, create_random_text)
from capytcha_server.utils.tokens import decode_data, encode_data
from capytcha_server.utils.upload import download_captcha, upload_captcha

captcha_routes = web.RouteTableDef()

# TODO: add auth
@captcha_routes.post('/captcha/get')
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
@captcha_routes.post('/captcha/check')
async def check_captcha(request: web.Request) -> web.Response:
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
