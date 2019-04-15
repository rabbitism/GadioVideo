import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

import crawler
from config import config
import text_processing
 
def create_frame(image_name, title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']
    img = cv2.imread(image_name)
    height = int(img.shape[0]/img.shape[1]*picture_width)
    if(height> config['height']-2*margin):
        height = config['height']-2*margin
        picture_width = int(img.shape[1]/img.shape[0]*height)
    img = cv2.resize(img, (picture_width, height))
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    pilimg = Image.fromarray(cv2img)

    frame = Image.new('RGB', size, color=config['background_color'])
    frame.paste(pilimg, (margin, margin))
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)
    print(content)

    y_offset = margin+title_font.getsize("Gg")[1]+content_font.getsize("Gg")[1]
    if('\n' in title):
        y_offset+=title_font.getsize(title)[1]

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font)
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return cv2charimg

def create_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']

    frame = Image.new('RGB', size, color=config['background_color'])
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)

    y_offset = margin+title_font.getsize("Gg")[1]+content_font.getsize("Gg")[1]
    if('\n' in title):
        y_offset+=title_font.getsize(title)[1]

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font) 
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return cv2charimg

def generate_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']

    frame = Image.new('RGBA', size, color=config['background_color'])
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)

    y_offset = margin+title_font.getsize("Gg")[1]+content_font.getsize("Gg")[1]
    if('\n' in title):
        y_offset+=title_font.getsize(title)[1]

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font) 
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = np.array(frame)
    return cv2charimg

def generate_frame(image_url, title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config["margin"]
    picture_width = config['picture_width']

    # Read image from file
    try:
        image = cv2.imread(image_url)
    except:
        return generate_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font)

    # expand image for background
    ratio = max(size[0] / image.shape[1], size[1] / image.shape[0])+0.01
    background_image = cv2.resize(image, (int(image.shape[1] * ratio), int(image.shape[0] * ratio)), interpolation=cv2.INTER_CUBIC)
    background_image = cv2.GaussianBlur(background_image, (255, 255), 255)
    left = int((background_image.shape[1] - size[0]) / 2)
    right = left + size[0]
    top = int((background_image.shape[0] - size[1]) / 2)
    bottom = top + size[1]

    # shrink image to fit in image area
    potential_height = config['height'] - margin * 2
    ratio = max(image.shape[1] / picture_width, image.shape[0] / potential_height)
    content_image = cv2.resize(image, (int(image.shape[1] / ratio), int(image.shape[0] / ratio)), interpolation=cv2.INTER_CUBIC)

    actual_width = int(image.shape[1] / ratio)

    # cut background image to fit frame size
    background_image = background_image[top:bottom, left:right]

    background_cv2img = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
    content_cv2img = cv2.cvtColor(content_image, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(background_cv2img).convert('RGBA')
    content_frame = Image.fromarray(content_cv2img)
    frame.paste(content_frame, (margin, margin))

    # add background for text area
    board = Image.new('RGBA', (size[0] - actual_width - int(margin * 1.5), config['height']), color=(255, 255, 255, 120))

    frame.paste(board, (actual_width+int(margin*1.5), 0), mask=board)
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-actual_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-actual_width-config['margin']*3)
    print(content)

    y_offset = margin+title_font.getsize("Gg")[1]+content_font.getsize("Gg")[1]
    if('\n' in title):
        y_offset+=title_font.getsize(title)[1]

    draw.text((actual_width+margin*2, margin), title, config['title_color'], font=title_font)
    draw.text((actual_width+margin*2, y_offset), content, config['content_color'], font=content_font)

    cv2charimg = np.array(frame)

    #cv2.imshow("Image", cv2charimg)
    #cv2.waitKey(0)
    #print("Hello")
    return cv2charimg

 
def main():
    print("Hello")
    font = ImageFont.truetype(config['font'], config['title_font_size'], encoding="utf-8")
    font2 = ImageFont.truetype(config['font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(font)
    content_wrapper = text_processing.Wrapper(font2)

    generate_frame("test\opencv-gaussian-blur.png", "Title","Content", (1280, 720),title_wrapper,content_wrapper,font,font2)
    
 
if __name__ == "__main__":
    main()