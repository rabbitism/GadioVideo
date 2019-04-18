import os
import sys

import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import Image, ImageDraw, ImageFont

import config
import crawler
import image_processing
import text_processing
from config import config


def main(title:str, skip_crawling:bool):
    title=str(title)
    if(not skip_crawling):
        crawler.main(title)
    print("Start to create video for {}".format(title))
    fps = config['fps']
    width = config['width']
    height = config['height']

    # Paths
    output_dir = os.sep.join([".", "output"])
    if not os.path.exists(output_dir):
        print("Folder", output_dir, 'does not exist. Creating...')
        os.makedirs(output_dir)
    resource_dir = os.sep.join([".", "resource", title])

    # Assets
    result = text_processing.load_data(title)
    title_font = ImageFont.truetype(config['title_font'], config['title_font_size'], encoding="utf-8")
    content_font = ImageFont.truetype(config['content_font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(title_font)
    content_wrapper = text_processing.Wrapper(content_font)

    
    # Video Properties
    fourcc = VideoWriter_fourcc(*'mp4v')
    video = VideoWriter(os.sep.join([output_dir, title+'_simple.mp4']), fourcc, float(fps), (width, height))

    # Create Video
    keys = list(map(int, result.keys()))
    if 0 not in keys:
        keys.append(0)
        frame = image_processing.create_blank_frame("", "", (width, height), title_wrapper, content_wrapper, title_font, content_font)
    else:
        key = "0"
        image = os.sep.join([resource_dir, str(key)+result[key]['image_suffix']])
        header = result[key]['header']
        content = result[key]['content']
        print("标题：{}".format(header))
        if(result[key]['image_suffix'] in ['.gif', '.GIF']):
            frame = image_processing.create_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
        else:
            frame = image_processing.create_frame(image, header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
            #os.remove(image)

    keys.sort()
    # Set last picture to be 20 seconds long
    keys.append(keys[len(keys)-1]+20)
    #print(keys)
    # Number of frames in this video
    total_length = keys[len(keys)-1]*fps

    index = 0
    for i in range(total_length):
        if(index+1>len(keys)-1):
            frame = image_processing.create_blank_frame("","", (width, height), title_wrapper, content_wrapper, title_font, content_font)
        elif (i/fps)>keys[index+1]:
            index+=1
            print("Processing {} frames out of {}".format(index, len(keys)-1))
            key = str(keys[index])
            image = os.sep.join([resource_dir, str(key)+result[key]['image_suffix']])
            header = result[key]['header']
            content = result[key]['content']
            print("标题：{}".format(header))
            if(result[key]['image_suffix'] in ['.gif', '.GIF']):
                frame = image_processing.create_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
            else:
                frame = image_processing.create_frame(image, header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
                #os.remove(image)
        else:
            pass
        video.write(frame)
    print("{} finished!".format(title))


if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("----------")
        print("Please speciy gadio number. Try to run this script like: ")
        print("&>python simple.py 100000")
        print("----------")
    else:
        title=str(sys.argv[1])
        skip_crawling = False
        if(len(sys.argv)>2):
            if("-s" in sys.argv):
                skip_crawling = True
        main(title, skip_crawling)
