from moviepy.editor import *


def get_audio_duration(audio_dir):
    audio = AudioFileClip(audio_dir)
    return audio.duration

def create_video_with_frame(frame, start, end):
    print("Creating video clip...", start, end)
    image_clip = ImageClip(frame, duration= end - start)
    image_clip = image_clip.fx(vfx.fadein, duration=0.5)
    image_clip = image_clip.fx(vfx.fadeout, duration=0.5)
    return image_clip