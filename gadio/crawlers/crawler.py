import json
import os
import re
import sys
import urllib.request

import requests
from bs4 import BeautifulSoup

from gadio.configs.config import config

api = "https://www.gcores.com/gapi/v1/radios/112068?include=category,media,djs,media.timelines"

#https://www.gcores.com/gapi/v1/radios?page[limit]=5&sort=-published-at

def print_config():
    
    print(config)

class Crawler():

    @staticmethod
    def crawl(gadio_id: int):
        """Get timeline and corresponding contents from Gcores website
        
        Arguments:
            gadio_id {int} -- gadio id in gcores websites. 
        """
        url = "https://www.gcores.com/gapi/v1/radios/" + str(gadio_id) + "?include=category,media,djs,media.timelines"
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
        