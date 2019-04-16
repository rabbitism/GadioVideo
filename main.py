import os
import sys

import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import Image, ImageDraw, ImageFont

import crawler
import image_processing
import text_processing
from config import config


def main(title:str):
    title = str(title)
    fps = config['fps']
    result, audio_url = crawler.crawler(title)
    width = config['width']
    height = config['height']
    for key in result.keys():
        image_name = str(key)
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        crawler.save_image(image_url, image_dir, image_name)
    fourcc = VideoWriter_fourcc(*'mp4v')
    output_dir = os.sep.join(['.','output'])
    if not os.path.exists(output_dir):
        print("Folder", output_dir, 'does not exist. Creating...')
        os.makedirs(output_dir)
    video = VideoWriter(os.sep.join([output_dir, str(title)+'.mp4']), fourcc, float(config['fps']), (config['width'], config['height']))
    font = ImageFont.truetype(config['font'], config['title_font_size'], encoding="utf-8")
    font2 = ImageFont.truetype(config['font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(font)
    content_wrapper = text_processing.Wrapper(font2)
    keys = list(result.keys())
    keys.append(0)
    keys.sort()
    keys.append(keys[len(keys)-1]+10)
    print(keys)
    frame = image_processing.create_blank_frame("", "", (width, height), title_wrapper, content_wrapper, font, font2)
    total_length = keys[len(keys)-1]*fps
    index = 0
    for i in range(total_length):
        if(index+1>len(keys)-1):
            frame = image_processing.create_blank_frame("", "", (width, height), title_wrapper, content_wrapper, font, font2)
        elif (i/fps) > keys[index+1]:
            index+=1
            print(index, "out of", len(keys))
            key = keys[index]
            image = image = os.sep.join(['.', 'resource', title, str(key)+text_processing.find_image_suffix(result[key]['image_url'])])
            header = result[key]['header']
            content = result[key]['content']
            print("标题：",header)
            if(result[key]['image_suffix'] in ['.gif', '.GIF']):
                frame = image_processing.create_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, font, font2)
            else:
                frame = image_processing.create_frame(image, header, content, (width, height), title_wrapper, content_wrapper, font, font2)
                os.remove(image)
        else:
            ""
        video.write(frame)
    print(title, "finished!")
    

        

if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("Must specify gadio number... ")
    else:
        title=str(sys.argv[1])
        main(title)
