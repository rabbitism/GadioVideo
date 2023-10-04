from gadio.configs.api import api
from gadio.text import text as text


class Image:

    def __init__(self, image_id, local_name):
        self.image_id = image_id
        self.image_url = api['image_url_template'].format(asset=self.image_id)
        self.suffix = text.find_image_suffix(image_id)
        self.local_name = str(local_name) + self.suffix

    @classmethod
    def load_from_url(cls, image_url, local_name):
        # Initialize a picture with non-standard gcores image url. image_identifier will be identical to image_url
        instance = Image(image_url, local_name)
        instance.image_url = image_url
        return instance


class Audio:
    def __init__(self, audio_id, local_name):
        self.audio_id = audio_id
        self.audio_url = api['audio_url_template'].format(asset=self.audio_id)
        self.suffix = text.find_image_suffix(self.audio_id)
        self.local_name = str(local_name) + self.suffix

    @classmethod
    def load_from_url(cls, audio_url, local_name):
        instance = Audio(audio_id=audio_url, local_name=local_name)
        instance.audio_url = audio_url
        return instance
