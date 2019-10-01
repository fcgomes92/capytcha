# ref: https://www.dev2qa.com/how-to-generate-random-captcha-in-python/
import random

from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha

from capytcha.utils import char_choices, numbers_list


def create_random_text(captcha_string_size=10):
    captcha_string_list = []
    captcha_string = ''
    for i in range(captcha_string_size):
        captcha_string = f'{captcha_string}{random.choice(char_choices)}'
    return captcha_string


def create_random_number(captcha_string_size=10):
    captcha_string_list = []
    captcha_string = ''
    for i in range(captcha_string_size):
        captcha_string = f'{captcha_string}{random.choice(numbers_list)}'
    return captcha_string


def create_image_captcha(captcha_text):
    image_captcha = ImageCaptcha(width=400, height=150)
    image_data = image_captcha.generate_image(captcha_text)
    image_captcha.create_noise_curve(image_data, image_data.getcolors())
    image_captcha.create_noise_dots(image_data, image_data.getcolors())

    # image_file = "./captcha_"+captcha_text + ".png"
    # image_captcha.write(captcha_text, image_file)

    return image_data


def create_audio_captcha(captcha_text):
    # Create the audio captcha with the specified voice wav file library folder.
    # Each captcha char should has it's own directory under the specified folder ( such as ./voices),
    # for example ./voices/a/a.wav will be played when the character is a.
    # If you do not specify your own voice file library folder, the default built-in voice library which has only digital voice file will be used.
    # audio_captcha = AudioCaptcha(voicedir='./voices')
    # Create an audio captcha which use digital voice file only.
    audio_captcha = AudioCaptcha()
    audio_data = audio_captcha.generate(captcha_text)

    # audio_file = "./captcha_"+captcha_text+'.wav'
    # audio_captcha.write(captcha_text, audio_file)

    return audio_data


if __name__ == '__main__':
    captcha_text = create_random_text()
    create_image_captcha(captcha_text)
    create_audio_captcha()
