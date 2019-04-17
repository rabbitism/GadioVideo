import math
import os
import sys

import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

import crawler
import image_processing
import text_processing
import video_processing
from config import config


def main(title:str, skip_crawling:bool):
    title=str(title)
    if(not skip_crawling):
        crawler.main(title)
    print("Start to create video for {}".format(title))
    fps = config['animation_fps']
    width = config['width']
    height = config['height']
    test = config['test']

    # Paths
    output_dir = os.sep.join([".", "output"])
    if not os.path.exists(output_dir):
        print("Folder", output_dir, 'does not exist. Creating...')
        os.makedirs(output_dir)
    resource_dir = os.sep.join([".", "resource", title])

    # Assets
    result = text_processing.load_data(title)
    title_font = ImageFont.truetype(config['font'], config['title_font_size'], encoding="utf-8")
    content_font = ImageFont.truetype(config['font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(title_font)
    content_wrapper = text_processing.Wrapper(content_font)
    audio_clip = AudioFileClip(os.sep.join([".", "resource", title, "audio", title + ".mp3"]))

    if not os.path.exists(output_dir):
        print("Folder", output_dir, 'does not exist. Creating...')
        os.makedirs(output_dir)

    keys = list(map(int, result.keys()))
    if 0 not in keys:
        keys.append(0)
    keys.append(math.ceil(audio_clip.duration))
    keys.sort()
    #print(keys)
    video_clips = []

    key_length = 10 if test else len(keys)-1

    files = os.listdir(os.sep.join(['.','resource', title]))
    print(files)
    
    for i in range(1, key_length):
        key = str(keys[i])
        start = keys[i]
        end = keys[i+1]
        #image_dir = os.sep.join(['.', 'resource', key+result[key]['image_suffix']])
        if((key not in result.keys()) or (key+result[key]['image_suffix'] not in files)):
            print("Case1")
            frame = image_processing.generate_blank_frame("", "", (width, height), title_wrapper, content_wrapper, title_font, content_font)
            videoclip = video_processing.create_video_with_frame(frame, start, end)
            video_clips.append(videoclip)
        else:
            if (result[key]['image_suffix'].lower() not in [".gif"]):
                print("Case2")
                image = os.sep.join(['.', 'resource', title, str(key)+result[key]['image_suffix']])
                header = result[key]['header']
                content = result[key]['content']
                frame = image_processing.generate_frame(image, header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
                videoclip = video_processing.create_video_with_frame(frame, start, end)
                video_clips.append(videoclip)
                #os.remove(image)
            elif(result[key]['image_suffix'].lower() in [".gif"]):
                print("Case3")
                image = os.sep.join(['.', 'resource', title, str(key)+result[key]['image_suffix']])
                print(image)
                header = result[key]['header']
                content = result[key]['content']
                if config['skip_gif']:
                    background_frame = image_processing.generate_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
                    videoclip = video_processing.create_video_with_frame(background_frame, start, end)
                else:
                    gif_clip = video_processing.load_gif_clip(image)
                    background_frame = image_processing.generate_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, title_font, content_font)
                    videoclip = video_processing.create_video_with_gif_clip(background_frame, gif_clip, start, end)
                video_clips.append(videoclip)


    merged_clips = concatenate_videoclips(video_clips)
    merged_clips.audio = audio_clip
    logo_clip = video_processing.load_logo(os.sep.join([".", "util", config['logo_name']]), duration = merged_clips.duration)
    if config['enable_logo']:
        final_clip = video_processing.add_logo(merged_clips, logo_clip)
    else:
        final_clip = merged_clips
    if test:
        final_clip = video_processing.add_logo(merged_clips, logo_clip).subclip(0, min(200, final_clip.duration))
    final_clip.write_videofile(os.sep.join([".", "output", title+"_animated.mp4"]), fps=fps, threads=4)
    print(title, "finished!")
    


if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("----------")
        print("Please speciy gadio number. Try to run this script like: ")
        print("&>python animated.py 100000")
        print("----------")
    else:
        title=str(sys.argv[1])
        skip_crawling = False
        if(len(sys.argv)>2):
            if("-s" in sys.argv):
                skip_crawling = True
        main(title, skip_crawling)
