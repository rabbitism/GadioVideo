import os

import cv2
import numpy as np
import pillow_avif
from PIL import Image, ImageDraw, ImageFont

from gadio.configs.config import config
from gadio.models.radio import Radio
from gadio.text.wrapper import Wrapper
from gadio.models.page import Page


class Frame:
    width = config['width']
    height = config['height']
    title_font = ImageFont.truetype(
        config['title_font'], config['title_font_size'], encoding="utf-8")
    content_font = ImageFont.truetype(
        config['content_font'], config['content_font_size'], encoding="utf-8")
    title_wrapper = Wrapper(title_font)
    content_wrapper = Wrapper(content_font)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_cover(radio: Radio):
        """create a cover page for start of video. No text pasted on this page.

        Arguments:
            radio {Radio} -- Radio

        Returns:
            image -- a cv2 frame.
        """
        cover_dir = os.sep.join(
            ['cache', str(radio.radio_id), radio.cover.local_name])
        print('Creating cover page')
        image = cv2.imread(cover_dir)
        image = Frame.expand_frame(image, Frame.width, Frame.height)
        return image

    @staticmethod
    def create_page(page: Page, radio: Radio):
        """Create a gadio page frame.
        Pipeline:
        1. Load image with opencv, use opencv to resize and blur.
        2. Convert opencv image to Pillow image
        3. Draw text on Pillow image
        4. Convert back to opencv image for opencv VideoWriter

        Beware that Pillow image and opencv channel orders are different.
        Arguments:
            page {Page} -- Gadio page

        Keyword Arguments:
            radio {Radio} -- radio

        Returns:
            np.array -- An numpy array representing cv2 image.
        """
        image_suffix = page.image.suffix
        if image_suffix == "" or image_suffix.lower() == '.gif':
            # If image is not found or image is gif, load cover as background
            image_dir = os.sep.join(['cache', str(radio.radio_id), radio.cover.local_name])
        else:
            image_dir = os.sep.join(['cache', str(radio.radio_id), page.image.local_name])
        qr_dir = os.sep.join(['cache', str(radio.radio_id), 'qr_quotes', page.image.local_name.split('.')[0] + ".png"])

        image = cv2.imread(image_dir)
        if image is None:
            match image_suffix:
                case '.avif':
                    pil_image = Image.open(image_dir)
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            # print(image_dir)
        image_suffix = page.image.suffix
        background_image = Frame.expand_frame(image, Frame.width, Frame.height)
        background_image = cv2.GaussianBlur(background_image, (255, 255), 255)
        content_image = Frame.shrink_frame(image, 550, 550)

        # Convert to PIL accepted RGB channel order
        background_rgb = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
        content_rgb = cv2.cvtColor(content_image, cv2.COLOR_BGR2RGB)

        # Convert to RGBA for transparency rendering
        frame = Image.fromarray(background_rgb).convert('RGBA')

        mask = Image.new('RGBA', (Frame.width, Frame.height), color=(0, 0, 0, 128))
        frame.paste(mask, (0, 0), mask=mask)

        left_offset = int(round(245 / 1920 * Frame.width)) + int(round((550 - content_image.shape[1]) / 2))
        top_offset = int(round(210 / 1080 * Frame.height)) + int(round((550 - content_image.shape[0]) / 2))

        content_frame = Image.fromarray(content_rgb)
        content_image_mask = Image.new('RGBA', (content_image.shape[1], content_image.shape[0]), color=(0, 0, 0, 26))
        if image_suffix == "" or image_suffix.lower() == '.gif':
            # if image is not properly downloaded or is gif, no content image should be added.
            print("GIF will not be rendered in this page...")
        else:
            frame.paste(content_frame, (left_offset, top_offset))
            frame.paste(content_image_mask, (left_offset, top_offset), mask=content_image_mask)

        try:
            logo_image = Image.open(config['gcores_logo_name']).convert('RGBA')
            qr_image = Image.open(config['gcores_qr_name']).convert('RGBA')
            logo_left_offset = int(round(120 / 1920 * Frame.width))
            logo_top_offset = int(round(52 / 1080 * Frame.height))
            qr_left_offset = logo_left_offset
            qr_top_offset = int(round(917 / 1080 * Frame.height))
            frame.paste(logo_image, (logo_left_offset, logo_top_offset), mask=logo_image)
            frame.paste(qr_image, (qr_left_offset, qr_top_offset), mask=qr_image)
            if os.path.exists(qr_dir):
                qr_right_offset = int(round(1700 / 1920 * Frame.width))
                page_qr_image = Image.open(qr_dir).convert('RGBA')
                page_qr_image = page_qr_image.resize((86, 86))
                frame.paste(page_qr_image, (qr_right_offset, qr_top_offset), mask=page_qr_image)
        except:
            print("Passing logo rendering due to file error")

        draw = ImageDraw.Draw(frame)

        text_width_limit = int(round(770 / 1920 * Frame.width))

        title_string = Frame.title_wrapper.wrap_string(page.title, text_width_limit)
        print('Title:', title_string)
        raw_content = page.content
        content_string = Frame.content_wrapper.wrap_string(raw_content, text_width_limit)
        # print(content_string)

        # Dimensions for text layout
        text_top_offset = int(round(260 / 1080 * Frame.height))
        text_left_offset = int(round(920 / 1920 * Frame.width))
        title_left, title_top, title_right, title_bottom = Frame.title_font.getbbox(title_string)
        title_height = title_bottom - title_top
        # title_height = Frame.title_font.getsize_multiline(title_string)[1]
        title_space_bottom = int(round(Frame.title_font.size * 0.9))
        content_height_limit = int(round(574 / 1080 * Frame.height)) - title_height - title_space_bottom

        content_space = int(round(Frame.content_font.size * 0.8))
        content_left, content_top, content_right, content_bottom = Frame.title_font.getbbox(content_string)
        actual_content_height = content_bottom - content_top
        # actual_content_height = Frame.content_font.getsize_multiline(content_string, spacing=content_space)[1]
        while actual_content_height > content_height_limit:
            Frame.content_font = Frame.shrink_font(Frame.content_font, config['content_font'])
            content_space = int(round(Frame.content_font.size * 0.8))
            content_wrapper = Wrapper(Frame.content_font)
            content_string = content_wrapper.wrap_string(raw_content, text_width_limit)
            content_left, content_top, content_right, content_bottom = Frame.title_font.getbbox(content_string)
            actual_content_height = content_bottom - content_top
            # actual_content_height = Frame.content_font.getsize_multiline(content_string, spacing=content_space)[1]
            # print(actual_content_height)

        print(content_string)
        draw.text((text_left_offset, text_top_offset), title_string, config['gcores_title_color'],
                  font=Frame.title_font)
        draw.text((text_left_offset, text_top_offset + title_height + title_space_bottom), content_string,
                  config['gcores_content_color'], font=Frame.content_font, spacing=content_space)

        # Reset content_wrapper and content_font
        Frame.content_font = ImageFont.truetype(config['content_font'], config['content_font_size'], encoding="utf-8")
        Frame.content_wrapper = Wrapper(Frame.content_font)

        cv2charimg = np.array(frame)
        result = cv2.cvtColor(cv2charimg, cv2.COLOR_RGB2BGR)

        return result

    @staticmethod
    def expand_frame(image, target_width, target_height):
        """Expand a frame so it is larger than the rectangle

        Arguments:
            image {Image} -- cv2 image
            target_width {int} -- target width of rectangle
            target_height {int} -- target width of rectangle

        Raises:
            NotImplementedError: [description]

        Returns:
            Image -- resized image
        """
        # shape[0]: height, shape[1]: width
        width_ratio = image.shape[1] / target_width
        height_ratio = image.shape[0] / target_height
        ratio = min(width_ratio, height_ratio)
        # in case width or height smaller than target after rounding.
        actual_width = max(int(image.shape[1] / ratio), target_width)
        actual_height = max(int(image.shape[0] / ratio), target_height)
        result = cv2.resize(image, (actual_width, actual_height),
                            interpolation=cv2.INTER_CUBIC)
        left = int((result.shape[1] - target_width) / 2)
        right = left + target_width
        top = int((result.shape[0] - target_height) / 2)
        bottom = top + target_height
        return result[top:bottom, left:right]

    @staticmethod
    def shrink_frame(image, target_width, target_height):
        """Shrink a frame so it is smaller than the rectangle

        Arguments:
            image {Image} -- np array
            target_width {int} -- target width of rectangle
            target_height {int} -- target height of rectangle

        Returns:
            np.array -- resized image
        """

        # shape[0] : height, shape[1]: width
        width_ratio = image.shape[1] / target_width
        height_ratio = image.shape[0] / target_height
        ratio = max(width_ratio, height_ratio)
        actual_width = min(int(image.shape[1] / ratio), target_width)
        actual_height = min(int(image.shape[0] / ratio), target_height)
        result = cv2.resize(image, (actual_width, actual_height), interpolation=cv2.INTER_CUBIC)
        return result

    @staticmethod
    def shrink_font(font, font_family):
        result_font = ImageFont.truetype(font_family, font.size - 2, encoding="utf-8")
        return result_font
