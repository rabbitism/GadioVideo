import crawler
import image_processing
import text_processing

import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

from config import config

def main(title:str):
    fps = config['fps']
    result = crawler.crawler(title)
    for key in result.keys():
        image_name = key
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        #crawler.save_image(image_url, image_dir, image_name)
    fourcc = VideoWriter_fourcc(*'mp4v')
    video = VideoWriter(os.sep.join(['.', 'resource', str(title)+'.mp4']), fourcc, float(config['fps']), (config['width'], config['height']))
    font = ImageFont.truetype("msyh.ttc", config['title_font_size'], encoding="utf-8")
    font2 = ImageFont.truetype("msyh.ttc", config['content_font_size'], encoding="utf-8") 
    wrapper = text_processing.Wrapper(font2)
    keys = list(result.keys())
    keys.append(0)
    keys.sort()
    keys.append(keys[len(keys)-1]+10)
    print(keys)
    frame = image_processing.create_blank_frame("", "", (1280, 720), wrapper, font, font2)
    total_length = keys[len(keys)-1]*fps
    index = 0
    for i in range(total_length):
        if(index+1>len(keys)-1):
            frame = image_processing.create_blank_frame("", "", (1280, 720), wrapper, font, font2)
        elif (i/fps) > keys[index+1]:
            index+=1
            print(index, "out of", len(keys))
            key = keys[index]
            image = image = os.sep.join(['.', 'resource', title, str(key)+text_processing.find_image_suffix(result[key]['image_url'])])
            header = result[key]['header']
            content = result[key]['content']
            if(text_processing.find_image_suffix(result[key]['image_url']) in ['.gif', '.GIF']):
                frame = image_processing.create_blank_frame(header, content, (1280, 720), wrapper, font, font2)
            else:
                frame = image_processing.create_frame(image, header, content, (1280, 720), wrapper, font, font2)
        else:
            ""
        video.write(frame)
    

        

if __name__ == "__main__":
    #title = str(108272)
    #result = crawler.crawler(title)
    #for key in result.keys():
    #    image_name = key
    #    image_url = result[key]['image_url']
    #    image_dir = os.sep.join([".", "resource", title])
    #    #crawler.save_image(image_url, image_dir, image_name)
    #fourcc = VideoWriter_fourcc(*'mp4v')
    #video = VideoWriter('.\\resource\\circle_noise.mp4', fourcc, float(config['fps']), (config['width'], config['height']))
    #font = ImageFont.truetype("msyh.ttc", config['title_font_size'], encoding="utf-8")
    #font2 = ImageFont.truetype("msyh.ttc", config['content_font_size'], encoding="utf-8") 
    #wrapper = text_processing.Wrapper(font2)
    #for key in result.keys():
    #    if(text_processing.find_image_suffix(result[key]['image_url'])=='.gif'):
    #        continue
    #    image = os.sep.join(['.', 'resource', title, str(key)+text_processing.find_image_suffix(result[key]['image_url'])])
    #    #print(image)
    #    header = result[key]['header']
    #    #content = wrapper.wrap_string(result[key]['content'], config['width']-config['picture_width']-config['margin']*3, 0, 0)
    #    content = result[key]['content']
    #    print(content)
    #    frame = image_processing.create_frame(image, header, content, (1280, 720), wrapper, font, font2)
    #    for i in range(60):
    #        video.write(frame)
    main(str(108272))