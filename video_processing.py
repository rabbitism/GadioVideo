from moviepy.editor import *

from config import config


def get_audio_duration(audio_dir):
    audio = AudioFileClip(audio_dir)
    return audio.duration

def create_video_with_frame(frame, start, end):
    print("Analyzing video clip...", start, end)
    image_clip = ImageClip(frame, duration= end - start)
    image_clip = (image_clip.fx(vfx.fadein, duration=config['fade_duration']/2).fx(vfx.fadeout, duration=config['fade_duration']/2))
    #image_clip = image_clip.fx(vfx.fadein, duration=config['fade_duration'] / 2)
    #image_clip = image_clip.fx(vfx.fadeout, duration=config['fade_duration'] / 2)
    
    return image_clip

def create_video_with_gif_clip(frame, clip, start, end):
    margin = config['margin']
    print("Analyzing video clip with gif...", start, end)
    image_clip = ImageClip(frame, duration=end - start)
    gif_clip = clip.fx(vfx.loop, duration=end - start)
    potential_width = config['picture_width']
    potential_height = config['height'] - margin * 2
    ratio = min(potential_height / gif_clip.h, potential_width / gif_clip.w)
    width = int(gif_clip.w * ratio)
    height = int(gif_clip.h * ratio)
    gif_clip = gif_clip.fx(vfx.resize, width=width, height=height)
    
    final_clip = CompositeVideoClip([image_clip, gif_clip.set_pos((margin, margin))])
    final_clip = final_clip.fx(vfx.fadein, duration=config['fade_duration'] / 2)
    final_clip = final_clip.fx(vfx.fadeout, duration=config['fade_duration'] / 2)
    return final_clip

def load_gif_clip(image_dir):
    try:
        video_clip = VideoFileClip(image_dir)
        #video_clip = video_clip.fx(vfx.loop, duration = duration)
        return video_clip
    except Exception as e:
        print("Error", e)

def load_logo(image_dir:str, duration:int):
    print("Analyzing logo image clip...")
    image_clip = ImageClip(image_dir, transparent=True, duration=duration)
    image_clip = image_clip.fx(vfx.resize, height=int(config['margin']*0.8))
    return image_clip

def add_logo(final_clip, logo_clip):
    return CompositeVideoClip([final_clip, logo_clip.set_pos((int(config['margin']*0.1),int(config['height']-config['margin'])))])

def main():
    clip = load_logo("./util/logo.png", 0, 10)
    clip2 = load_logo("./test/Sample.jpg", 0, 10)
    clip3 = load_gif_clip("./test/gif.gif")
    clip_final = CompositeVideoClip([clip2, clip, clip3])
    clip_final.write_videofile("./test/test.mp4", fps=24)

if __name__ == "__main__":
    main()