import json
import os
import re
import sys
import urllib.request

import requests

from gadio.configs.config import config
from gadio.models.asset import Image, Audio
from gadio.models.radio import Radio
from gadio.models.user import User
from gadio.models.page import Page
from gadio.configs.api import api

#api = "https://www.gcores.com/gapi/v1/radios/112068?include=category,media,djs,media.timelines"

class Crawler():

    @staticmethod
    def crawl(gadio_id: int):
        """Get timeline and corresponding contents from Gcores website
        
        Arguments:
            gadio_id {int} -- gadio id in gcores websites. 
        """
        url = api['radio_api_template'].format(radio_id=gadio_id)
        print("Extracting information from ", gadio_id)
        content = requests.get(url).content
        parsed = json.loads(content)
        #print(parsed)
        dictionary = dict()
        for i in parsed['included']:
            if (i['type'] in dictionary.keys()):
                dictionary[i['type']] += 1
            else:
                dictionary[i['type']] = 1
        print(dictionary)
        with open("test.json", 'w', encoding='utf-8') as outfile:
            json.dump(parsed, outfile, ensure_ascii=False, indent=4)
        return parsed
        
    @staticmethod
    def download_image(image: Image, file_dir: str):
        try:
            if not os.path.exists(file_dir):
                print("Folder", file_dir, 'does not exist. Creating...')
                os.makedirs(file_dir)
            print("Saving image to", image.local_name)
            r = urllib.request.urlretrieve(image.image_url, file_dir + os.sep + image.local_name)
            return 1
        except Exception as e:
            print("Error", e)
            return 0

    @staticmethod
    def download_audio(audio: Audio, file_dir: str):
        try:
            if not os.path.exists(file_dir):
                print("Folder", file_dir, 'does not exist. Creating...')
                os.makedirs(file_dir)
            print("Saving audio to", audio.local_name)
            r = urllib.request.urlretrieve(audio.audio_url, file_dir + os.sep + audio.local_name)
            return 1
        except Exception as e:
            print("Error", e)
            return 0
        return

    @staticmethod
    def download_assets(radio: Radio, file_dir: str):
        id = str(radio.radio_id)
        file_dir = file_dir + os.sep + id
        Crawler.download_image(radio.cover, file_dir)
        Crawler.download_audio(radio.audio, file_dir + os.sep + 'audio')
        for user in radio.users:
            Crawler.download_image(user.portrait, file_dir + os.sep + 'users')
            
        for page in radio.timeline.values():
            Crawler.download_image(page.image, file_dir)

