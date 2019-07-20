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
from gadio.text.text import *

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
        cache_dir = os.sep.join([os.curdir, 'cache', str(gadio_id)])
        if not os.path.exists(cache_dir):
            print("Folder", cache_dir, 'does not exist. Creating...')
            os.makedirs(cache_dir)
        with open(cache_dir+os.sep+'data.json', 'w', encoding='utf-8') as outfile:
            print(cache_dir)
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

    @staticmethod
    def get_latest():
        url = api['radio_list_api_template']
        print("Getting the latest gadio id...")
        content = requests.get(url).content
        parsed = json.loads(content)
        id = parsed['data'][0]['id']
        return int(id)
    
    def get_headers(radio: Radio):
        offset = config['start_offset']
        headers = []
        for i in radio.timestamps:
            if (i not in radio.timeline.keys()):
                continue
            else:
                seconds = i + 1 if i == 0 else i
                time = seconds_to_time(str(seconds + offset))
                headers.append(time + " " + radio.timeline[i].title)
        with open(os.sep.join(['.', "output", radio.radio_id + "_headers.txt"]), 'w+', encoding='utf-8') as links:
            length = 0
            last = ""
            for header in headers:
                line= header+"⭐"
                length+=len(line)
                if(length>990): # Bilibili comment length 1000
                    links.write("\n\n")
                    length=len(line)
                links.writelines(line)
        links.close()