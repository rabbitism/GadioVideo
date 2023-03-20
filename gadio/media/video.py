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
        if not os.path.exists(images_loc):
            os.makedirs(images_loc)
        vclips_loc = os.path.join(os.curdir, 'cache', str(radio.radio_id), 'videos')
        if not os.path.exists(vclips_loc):
            os.makedirs(vclips_loc)
        textlist = vclips_loc + os.sep + 'list.txt'
        if os.path.exists(textlist):
            os.remove(textlist)
            
        if not os.path.exists(Video.output_dir):
            print("Folder", Video.output_dir, 'does not exist. Creating...')
            os.makedirs(Video.output_dir)
        clip_count = len(radio.timestamps) - 1
        
        for i in range(clip_count):
            if (radio.timestamps[i] not in radio.timeline.keys()):
                print(radio.timestamps[i], "has no corresponding image, load cover as backup")
                frame = Frame.create_cover(radio)
            else:
                frame = Frame.create_page(radio.timeline[radio.timestamps[i]], radio)
                
            sequence = '%05d' % i
            frame_time = str(radio.timestamps[i + 1] - radio.timestamps[i])
            
            Image.fromarray(frame).save(images_loc + os.sep + sequence + '.png')
            sp.run([ffdl.ffmpeg_path, 
                    '-r', str(Video.fps), 
                    '-loop', '1', 
                    '-i', images_loc + os.sep + sequence + '.png', 
                    '-c:v', 'libx264', 
                    '-pix_fmt', 'yuv420p', 
                    '-crf', '24', 
                    '-t', frame_time, 
                    vclips_loc + os.sep + sequence + '.mp4'])
            
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
                Video.output_dir + os.sep + radio.title + '.mp4'])
        
        print("{} finished!".format(radio.title))
        # rmtree(os.path.join(os.curdir, 'cache', str(radio.radio_id), 'images'))
        # rmtree(os.path.join(os.curdir, 'cache', str(radio.radio_id), 'videos'))