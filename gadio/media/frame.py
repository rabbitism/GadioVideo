
import os

import cv2
import numpy as np
from cv2 import VideoWriter_fourcc
from PIL import Image, ImageDraw, ImageFont

from gadio.configs.config import config
from gadio.models.radio import Radio
from gadio.text.wrapper import Wrapper


class Frame():
    width = config['width']
    height = config['height']
    title_font = ImageFont.truetype(config['title_font'], config['title_font_size'], encoding="utf-8")
    content_font = ImageFont.truetype(config['content_font'], config['content_font_size'], encoding="utf-8")
    title_wrapper = Wrapper(title_font)
    content_wrapper = Wrapper(content_font)

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    @staticmethod
    def create_cover(radio:Radio):
        cover_dir = os.sep.join(['cache', str(radio.radio_id), radio.cover.local_name])
        print(cover_dir)
        image = cv2.imread(cover_dir)
        image = Frame.shrink_frame(image, Frame.width, Frame.height)
        print(image)
        #raise NotImplementedError

    @staticmethod
    def shrink_frame(image, target_width, target_height):
        image = cv2.resize(image, (int(image.shape[1] * 1.2), int(image.shape[0] * 1.2)), interpolation=cv2.INTER_CUBIC)
        return image
        #raise NotImplementedError
