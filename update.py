import crawler
import image_processing
import text_processing
import video_processing

import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import sys
from moviepy.editor import *
import math

from config import config

def update(title:str):
    title = str(title)
    fps = config['fps']
    result, audio_url = crawler.crawler(title)
    width = config['width']
    height = config['height']
    for key in result.keys():
        image_name = str(key)
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        #crawler.save_image(image_url, image_dir, image_name)
    
    #crawler.save_audio(audio_url, os.sep.join([".", "resource", title, "audio"]), title)
    audio_clip = AudioFileClip(os.sep.join([".", "resource", title, "audio", title + ".mp3"]))
    print(audio_clip.duration)

    fourcc = VideoWriter_fourcc(*'mp4v')
    output_dir = os.sep.join(['.', 'output'])
    
    if not os.path.exists(output_dir):
        print("Folder", output_dir, 'does not exist. Creating...')
        os.makedirs(output_dir)

    font = ImageFont.truetype(config['font'], config['title_font_size'], encoding="utf-8")
    font2 = ImageFont.truetype(config['font'], config['content_font_size'], encoding="utf-8") 
    title_wrapper = text_processing.Wrapper(font)
    content_wrapper = text_processing.Wrapper(font2)
    keys = list(result.keys())
    if 0 not in keys:
        keys.append(0)
    keys.append(math.ceil(audio_clip.duration))
    keys.sort()
    print(keys)
    frame = image_processing.create_blank_frame("", "", (width, height), title_wrapper, content_wrapper, font, font2)
    video_clips = []
    
    #for i in range(10):
    for i in range(len(keys)-1):
        key = keys[i]
        #print(result[key]['image_suffix'])
        if (key == 0):
            if(key not in result.keys()):
                frame = image_processing.create_blank_frame("", "", (width, height), title_wrapper, content_wrapper, font, font2)
                videoclip = video_processing.create_video_with_frame(frame, 0, keys[1])
                video_clips.append(videoclip)
            else:
                image = os.sep.join(['.', 'resource', title, str(key)+result[key]['image_suffix']])
                header = result[key]['header']
                content = result[key]['content']
                frame = image_processing.generate_frame(image, header, content, (width, height), title_wrapper, content_wrapper, font, font2)
                videoclip = video_processing.create_video_with_frame(frame, keys[i], keys[i + 1])
                video_clips.append(videoclip)
        elif (result[key]['image_suffix'].lower() not in [".gif"]):
            image = os.sep.join(['.', 'resource', title, str(key)+result[key]['image_suffix']])
            header = result[key]['header']
            content = result[key]['content']
            frame = image_processing.generate_frame(image, header, content, (width, height), title_wrapper, content_wrapper, font, font2)
            videoclip = video_processing.create_video_with_frame(frame, keys[i], keys[i + 1])
            video_clips.append(videoclip)
        elif(result[key]['image_suffix'].lower() in [".gif"]):
            image = os.sep.join(['.', 'resource', title, str(key)+result[key]['image_suffix']])
            header = result[key]['header']
            content = result[key]['content']
            gif_clip = video_processing.load_gif_clip(image)
            background_frame = image_processing.generate_blank_frame(header, content, (width, height), title_wrapper, content_wrapper, font, font2)
            videoclip = video_processing.create_video_with_gif_clip(background_frame, gif_clip, keys[i], keys[i + 1])
            video_clips.append(videoclip)
        else:
            background_frame = image_processing.generate_blank_frame("", "", (width, height), title_wrapper, content_wrapper, font, font2)
            videoclip = video_processing.create_video_with_frame(frame, keys[i], keys[i + 1])
            video_clips.append(videoclip)



    merged_clips = concatenate_videoclips(video_clips)
    merged_clips.audio = audio_clip
    logo_clip = video_processing.load_logo(os.sep.join([".", "util", config['logo_name']]), duration = merged_clips.duration)
    final_clip = video_processing.add_logo(merged_clips, logo_clip)
    #final_clip = video_processing.add_logo(merged_clips, logo_clip).subclip(0, min(200, final_clip.duration))

    final_clip.write_videofile(os.sep.join([".", "output", title+".mp4"]), fps=3)
    print(title, "finished!")
    

        

if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("Must specify gadio number... ")
    else:
        title=str(sys.argv[1])
        update(title)