import video_processing

import os

audio_dir = os.sep.join([".", "test", "test.mp3"])
a = video_processing.get_audio_duration(audio_dir)
print(a)