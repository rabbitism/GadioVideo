from cv2 import VideoWriter
from moviepy.editor import *

from gadio.configs.config import config
from gadio.media.frame import Frame
from gadio.models.radio import Radio
import re

class Video:
    fourcc = VideoWriter.fourcc(*'mp4v')
    fps = int(config['fps'])
    width = config['width']
    height = config['height']
    output_dir = os.sep.join(['.', 'output'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_video(radio: Radio):
        if not os.path.exists(Video.output_dir):
            print("Folder", Video.output_dir, 'does not exist. Creating...')
            os.makedirs(Video.output_dir)
        video = VideoWriter(Video.output_dir + os.sep + str(radio.radio_id) + '_temp.mp4', Video.fourcc, Video.fps,
                            (Video.width, Video.height))
        clip_count = len(radio.timestamps) - 1
        for i in range(clip_count):
            if radio.timestamps[i] not in radio.timeline.keys():
                print(radio.timestamps[i], "has no corresponding image, load cover as backup")
                frame = Frame.create_cover(radio)
            else:
                frame = Frame.create_page(radio.timeline[radio.timestamps[i]], radio)
            frame_count = (radio.timestamps[i + 1] - radio.timestamps[i]) * Video.fps
            for j in range(frame_count):
                video.write(frame)
        video.release()

        cache_dir = os.sep.join(['.', 'cache', str(radio.radio_id)])
        video_clip = VideoFileClip(Video.output_dir + os.sep + str(radio.radio_id) + '_temp.mp4')
        print(video_clip.duration)
        audio_clip = AudioFileClip(os.sep.join(['.', 'cache', str(radio.radio_id), 'audio', radio.audio.local_name]))
        video_clip.audio = audio_clip
        if config['test']:
            video_clip = video_clip.subclip(0, min(200, video_clip.duration))

        # 删除字符串中的特殊字符
        valid_title = re.sub(r'[\\/*?:"<>|]', '', radio.title.replace('|', '丨'))
        file_name = '{} {}.mp4'.format(str(radio.radio_id), valid_title)
        file_path = os.sep.join([Video.output_dir, file_name])
        video_clip.write_videofile(file_path, fps=Video.fps)
        print("{} finished!".format(radio.title))
        os.remove(Video.output_dir+os.sep+str(radio.radio_id)+'_temp.mp4')
