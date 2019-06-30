import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

import crawler
from config import config
import text_processing

# create_frame is used for simple version videos, with no backgrounds. 
def create_frame(image_name, title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']
    raw_content = content
    image = cv2.imread(image_name)
    height = int(image.shape[0]/image.shape[1]*picture_width)
    if(height> config['height']-2*margin):
        height = config['height']-2*margin
        picture_width = int(image.shape[1]/image.shape[0]*height)
    frame = Image.new('RGB', size, color=config['background_color'])

    # shrink image to fit in image area
    potential_height = config['height'] - margin * 2
    ratio = max(image.shape[1] / picture_width, image.shape[0] / potential_height)
    content_image = cv2.resize(image, (int(image.shape[1] / ratio), int(image.shape[0] / ratio)), interpolation=cv2.INTER_CUBIC)

    actual_width = int(image.shape[1] / ratio)

    cv2img = cv2.cvtColor(content_image, cv2.COLOR_BGR2RGB) 
    pilimg = Image.fromarray(cv2img)

    frame.paste(pilimg, (margin, margin))

    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)
    print(content)

    potential_height = config['height'] - margin * 2
    y_offset = margin*1.5+title_font.getsize_multiline(title)[1]
    content_height = potential_height-y_offset+margin
    actual_content_height = content_font.getsize_multiline(content)[1]
    while(actual_content_height>content_height):
        content_font = shrink_font(content_font, config['content_font'])
        content_wrapper = text_processing.Wrapper(content_font)
        content = content_wrapper.wrap_string(raw_content, config['width'] -config['picture_width']-config['margin']*3)
        print(content)
        actual_content_height = content_font.getsize_multiline(content)[1]
        print(actual_content_height)

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font)
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return cv2charimg

# create_frame is used for simple version videos, with no backgrounds. 
def create_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']
    raw_content = content
    frame = Image.new('RGB', size, color=config['background_color'])
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)

    potential_height = config['height'] - margin * 2
    y_offset = margin*1.5+title_font.getsize_multiline(title)[1]
    content_height = potential_height-y_offset+margin
    actual_content_height = content_font.getsize_multiline(content)[1]
    while(actual_content_height>content_height):
        content_font = shrink_font(content_font, config['content_font'])
        content_wrapper = text_processing.Wrapper(content_font)
        content = content_wrapper.wrap_string(raw_content, config['width'] -config['picture_width']-config['margin']*3)
        print(content)
        actual_content_height = content_font.getsize_multiline(content)[1]
        print(actual_content_height)

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font) 
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return cv2charimg

# generate_frame is used for animated version videos
def generate_frame(image_url, title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config["margin"]
    picture_width = config['picture_width']
    raw_content = content
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
    # to resize image to fit in a rect of (WL, HL), with WL as width_limit and HL as height_limit
    # if there's a ratio R that resizes original edges of the image into the fitness
    # it has to be W' = W*R <= WL, H' = H*R <= HL, then it becomes R <= WL/W && R <= HL/H
    # Thus leads to R <= min(WL/W, HL/H)
    width_limit = int(round(550/1920 * size[0]))
    height_limit = int(round(550/1080 * size[1]))
    ratio = min(width_limit / image.shape[1], height_limit / image.shape[0])
    actual_width = int(round(image.shape[1] * ratio))
    actual_height = int(round(image.shape[0] * ratio))
    content_image = cv2.resize(image, (actual_width, actual_height), interpolation=cv2.INTER_CUBIC)

    # cut background image to fit frame size
    background_image = background_image[top:bottom, left:right]

    background_cv2img = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
    content_cv2img = cv2.cvtColor(content_image, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(background_cv2img).convert('RGBA')

    # add black mask on top of background
    board = Image.new('RGBA', size, color=(0, 0, 0, 128))
    frame.paste(board, (0, 0), mask=board)
 
    left_offset = int(round(245/1920 * size[0])) + int(round((width_limit - actual_width)/2))
    top_offset = int(round(210/1080 * size[1])) + int(round((height_limit - actual_height)/2))
    content_frame = Image.fromarray(content_cv2img)
    frame.paste(content_frame, (left_offset, top_offset))
    content_image_mask = Image.new('RGBA', (actual_width, actual_height), color=(0, 0, 0, 26))
    frame.paste(content_image_mask, (left_offset, top_offset), mask=content_image_mask)
    
    if config['enable_logo']:
        try:
            logo_image = Image.open(os.sep.join([".", "util", config['gcores_logo_name']])).convert('RGBA')
            qr_image = Image.open(os.sep.join([".", "util", config['gcores_qr_name']])).convert('RGBA')
            logo_left_offset = int(round(120/1920 * config['width']))
            logo_top_offset = int(round(52/1080 * config['height']))
            qr_left_offset = logo_left_offset
            qr_top_offset = int(round(917/1080 * config['height']))
            frame.paste(logo_image, (logo_left_offset, logo_top_offset), mask=logo_image)
            frame.paste(qr_image, (qr_left_offset, qr_top_offset), mask=qr_image)
        except:
            print("Passing logo rendering due to file error")

    draw = ImageDraw.Draw(frame)
    text_width_limit = int(round(770/1920 * size[0]))
    title = title_wrapper.wrap_string(title, text_width_limit)
    content = content_wrapper.wrap_string(content, text_width_limit)
    print(content)

    top_offset = int(round(260/1080 * size[1]))
    left_offset = int(round(920/1920 * size[0]))
    title_height = title_font.getsize_multiline(title)[1]
    title_space_bottom = int(round(title_font.size * 0.9))
    content_height_limit = int(round(574/1080 * size[1])) - title_height - title_space_bottom
    content_space = int(round(content_font.size * 0.8))
    actual_content_height = content_font.getsize_multiline(content, spacing=content_space)[1]
    while (actual_content_height>content_height_limit):
        content_font = shrink_font(content_font, config['content_font'])
        content_space = int(round(content_font.size * 0.8))
        content_wrapper = text_processing.Wrapper(content_font)
        content = content_wrapper.wrap_string(raw_content, text_width_limit)
        print(content)
        actual_content_height = content_font.getsize_multiline(content, spacing=content_space)[1]
        print(actual_content_height)

    print("Out")
    draw.text((left_offset, top_offset), title, config['gcores_title_color'], font=title_font)
    draw.text((left_offset, top_offset+title_height+title_space_bottom), content, config['gcores_content_color'], font=content_font, spacing=content_space)

    cv2charimg = np.array(frame)

    return cv2charimg

# generate_frame is used for animated version videos
def generate_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    margin = config['margin']
    picture_width = config['picture_width']
    raw_content = content
    frame = Image.new('RGBA', size, color=config['background_color'])
 
    draw = ImageDraw.Draw(frame)
    title = title_wrapper.wrap_string(title, config['width']-picture_width-config['margin']*3)
    content = content_wrapper.wrap_string(content, config['width']-picture_width-config['margin']*3)

    potential_height = config['height'] - margin * 2
    y_offset = margin*1.5+title_font.getsize_multiline(title)[1]
    content_height = potential_height-y_offset+margin
    actual_content_height = content_font.getsize_multiline(content)[1]

    while(actual_content_height>content_height):
        print("Too much information to display, Shrinking font size...")
        content_font = shrink_font(content_font, config['content_font'])
        content_wrapper = text_processing.Wrapper(content_font)
        content = content_wrapper.wrap_string(raw_content, config['width'] -config['picture_width']-config['margin']*3)
        print(content)
        actual_content_height = content_font.getsize_multiline(content)[1]
        #print(actual_content_height)

    draw.text((picture_width+margin*2, margin), title, config['title_color'], font=title_font) 
    draw.text((picture_width+margin*2, y_offset), content, config['content_color'], font=content_font) 
    cv2charimg = np.array(frame)
    return cv2charimg
    
def generate_title_image(image_dir, size):
    image = generate_cv2_title_image(image_dir, size)
    #print(image)
    frame = Image.fromarray(image).convert('RGBA')
    return np.array(frame)

#generate_cv2_frame is used for complex verison video.
def generate_cv2_frame(image_url, title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    frame = generate_frame(image_url, title, content, size, title_wrapper, content_wrapper, title_font, content_font)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#generate_cv2_frame is used for complex verison video.
def generate_cv2_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font):
    frame = generate_blank_frame(title, content, size, title_wrapper, content_wrapper, title_font, content_font)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def generate_cv2_title_image(image_dir, size):
    margin = config["margin"]
    # Read image from file
    try:
        image = cv2.imread(image_dir)
    except:
        image = np.zeros((size[0],size[1],3), np.uint8)
        # 使用白色填充图片区域,默认为黑色
        image.fill(255)

    # expand image for background
    ratio = max(size[0] / image.shape[1], size[1] / image.shape[0])+0.01
    background_image = cv2.resize(image, (int(image.shape[1] * ratio), int(image.shape[0] * ratio)), interpolation=cv2.INTER_CUBIC)
    left = int((background_image.shape[1] - size[0]) / 2)
    right = left + size[0]
    top = int((background_image.shape[0] - size[1]) / 2)
    bottom = top + size[1]

    # cut background image to fit frame size
    background_image = background_image[top:bottom, left:right]
    return background_image

def shrink_font(font, font_family):
    result_font = ImageFont.truetype(font_family, font.size-2, encoding="utf-8")
    print(result_font.size)
    return result_font


 
def main():
    print("Hello")
    font = ImageFont.truetype(config['font'], config['title_font_size'], encoding="utf-8")
    font2 = ImageFont.truetype(config['font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(font)
    content_wrapper = text_processing.Wrapper(font2)

    generate_frame("test\opencv-gaussian-blur.png", "Title","Content", (1280, 720),title_wrapper,content_wrapper,font,font2)
    
 
if __name__ == "__main__":
    main()
    font = ImageFont.truetype("msyh.ttc", 40, encoding="utf-8") 
    font.getsize_multiline
