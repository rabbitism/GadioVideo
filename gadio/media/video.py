from PIL import Image
import subprocess as sp
import os
# from shutil import rmtree
import ffmpeg_downloader as ffdl

from gadio.configs.config import config
from gadio.media.frame import Frame
from gadio.models.radio import Radio


class Video():

    fps = config['fps']
    width = config['width']
    height = config['height']
    output_dir = os.path.join('.', 'output')

    def __init__(self, config, *args, **kwargs):
        return super().__init__(config, *args, **kwargs)

    @staticmethod
    def create_video(radio: Radio):
        images_loc = os.path.join(os.curdir, 'cache', str(radio.radio_id), 'images')
        os.makedirs(images_loc, exist_ok=True)
        vclips_loc = os.path.join(os.curdir, 'cache', str(radio.radio_id), 'videos')
        os.makedirs(vclips_loc, exist_ok=True)
        textlist = os.path.join(vclips_loc, 'list.txt')
        if os.path.exists(textlist):
            os.remove(textlist)
            
        os.makedirs(Video.output_dir, exist_ok=True)
        clip_count = len(radio.timestamps) - 1
        
        for i in range(clip_count):
            if (radio.timestamps[i] not in radio.timeline.keys()):
                print(radio.timestamps[i], "has no corresponding image, load cover as backup")
                frame = Frame.create_cover(radio)
            else:
                frame = Frame.create_page(radio.timeline[radio.timestamps[i]], radio)
                
            sequence = '%05d' % i
            frame_time = str(radio.timestamps[i + 1] - radio.timestamps[i])
            
            Image.fromarray(frame).save(os.path.join(images_loc, sequence + '.png'))
            sp.run([ffdl.ffmpeg_path, 
                    '-r', str(Video.fps), 
                    '-loop', '1', 
                    '-i', os.path.join(images_loc, sequence + '.png'), 
                    '-c:v', 'libx264', 
                    '-pix_fmt', 'yuv420p', 
                    '-crf', '24', 
                    '-t', frame_time, 
                    os.path.join(vclips_loc, sequence + '.mp4')])
            
            with open(textlist, 'a+') as f:
                f.write("file '{}'\n".format(sequence + '.mp4'))
        f.close()

        audio_clip = os.path.join('.', 'cache', str(radio.radio_id), 'audio', radio.audio.local_name)
        sp.run([ffdl.ffmpeg_path, 
                '-f', 'concat', 
                '-safe', '0', 
                '-i', textlist, 
                '-i', audio_clip, 
                '-c:v', 'copy', 
                '-c:a', 'aac', 
                os.path.join(Video.output_dir, radio.title + '.mp4')])
        
        print("{} finished!".format(radio.title))
        # rmtree(os.path.join(os.curdir, 'cache', str(radio.radio_id), 'images'))
        # rmtree(os.path.join(os.curdir, 'cache', str(radio.radio_id), 'videos'))