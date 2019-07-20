from cv2 import VideoWriter, VideoWriter_fourcc
from moviepy.editor import *

from gadio.configs.config import config
from gadio.media.frame import Frame
from gadio.models.radio import Radio


class Video():

    fourcc = VideoWriter_fourcc(*'mp4v')
    fps = config['fps']
    width = config['width']
    height = config['height']
    output_dir = os.sep.join(['.', 'output'])

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    @staticmethod
    def create_video(radio: Radio):
        if not os.path.exists(Video.output_dir):
            print("Folder", Video.output_dir, 'does not exist. Creating...')
            os.makedirs(Video.output_dir)
        video = VideoWriter(Video.output_dir + os.sep + str(radio.radio_id) + '_temp.mp4', Video.fourcc, Video.fps, (Video.width, Video.height))
        clip_count = len(radio.timestamps) - 1
        for i in range(clip_count):
            if (radio.timestamps[i] not in radio.timeline.keys()):
                print(radio.timeline.keys())
                frame = Frame.create_cover(radio)
            else:
                frame = Frame.create_page(radio.timeline[radio.timestamps[i]], radio)
            frame_count = (radio.timestamps[i + 1] - radio.timestamps[i]) * Video.fps
            for j in range(frame_count):
                video.write(frame)
        video.release()

        video_clip = VideoFileClip(Video.output_dir + os.sep + str(radio.radio_id) + '_temp.mp4')
        print(video_clip.duration)
        audio_clip = AudioFileClip(os.sep.join(['.', 'cache', str(radio.radio_id), 'audio', radio.audio.local_name]))
        video_clip.audio = audio_clip
        if config['test']:
            video_clip = video_clip.subclip(0, min(200, video_clip.duration))
        video_clip.write_videofile(Video.output_dir +os.sep+ str(radio.radio_id)+" "+radio.title +".mp4", fps=Video.fps)
        print("{} finished!".format(radio.title))
        os.remove(Video.output_dir+os.sep+str(radio.radio_id)+'_temp.mp4')
