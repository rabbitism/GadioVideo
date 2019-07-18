import json
import os
import re
import sys
import urllib.request

import requests
from bs4 import BeautifulSoup

import text_processing
from config import config
import json


def crawler(number):
    """Get timeline and corresponding contents from Gcores webiste.
    
    Arguments:
        number {str} -- gadio number
    
    Returns:
        dict, str -- a dictionary in this format: {10:{'header':'标题', 'content':'内容', 'image_url':'https://......123.jpg','image_suffix':'.jpg'}}
    """

    # Get timelines
    url = "https://www.gcores.com/gapi/v1/radios/"+str(number)+"?include=media,media.timelines"
    content = requests.get(url).content
    parsed = json.loads(content)
    radio = parsed.get('data')
    included = parsed.get('included')
    media = radio.get('relationships').get('media').get('data')
    media = next(e for e in included if e.get('type') == media.get('type') and e.get('id') == media.get('id'))
    timelines = media.get('relationships').get('timelines').get('data')

    result = dict()
    for item in timelines:
        line = next(e for e in included if e.get('type') == item.get('type') and e.get('id') == item.get('id'))
        title = line.get('attributes').get('title')
        content = line.get('attributes').get('content')
        at = line.get('attributes').get('at')
        asset = 'https://image.gcores.com/'+str(line.get('attributes').get('asset'))
        asset_suffix = text_processing.find_image_suffix(asset)
        link = line.get('quote-href', '')
        result[at] = { 'header': title, 'content': content, 'image_url': asset, 'image_suffix': asset_suffix, 'link': link }
    
    audio = 'https://alioss.gcores.com/uploads/audio/'+str(media.get('attributes').get('audio'))
    cover = 'https://image.gcores.com/'+str(radio.get('attributes').get('thumb'))
    return result, audio, cover

def save_image(image_url, image_dir, image_name):
    """Save image from image_url to image_dir with name as image_name
    
    Arguments:
        image_url {string} -- image location from website
        image_dir {str} -- image destination
        image_name {str} -- name of image
    
    Returns:
        None -- no return
    """
    try:
        if not os.path.exists(image_dir):
            print("Folder", image_dir, 'does not exist. Creating...')
            os.makedirs(image_dir)
        file_suffix = re.match(".*(\..*)", image_url).group(1)
        print("Saving image to", image_name+file_suffix)
        r = urllib.request.urlretrieve(image_url, image_dir+os.sep+image_name+file_suffix)
        return 1
    except Exception as e:
        print("Error", e)
        return 0

def save_audio(audio_url, audio_dir, audio_name):
    try:
        if not os.path.exists(audio_dir):
            print("Folder", audio_dir, "does not exist. Creating...")
            os.makedirs(audio_dir)
        print("Saving audio to", audio_name + ".mp3")
        r = urllib.request.urlretrieve(audio_url, audio_dir + os.sep + audio_name + ".mp3")
    except Exception as e:
        print("Error", e)
        print("Audio file not saved. Please consider manually add audio file to folder {}, rename it as {} for video editing...".format(audio_dir, audio_name+".mp3"))

def main(title:str):
    """
    When excuting individually, this function will crawl all materials including pictures, audios, text, for specific gadio title. 
    """
    title = str(title)
    result, audio_url, title_url = crawler(title)
    test = config['test']
    count = 0
    for key in result.keys():
        image_name = str(key)
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        count+=save_image(image_url, image_dir, image_name)

    """Extract reference links and write to file""" 
    text_processing.extract_links(result, title)
    text_processing.extract_headers(result, title)
       
    save_audio(audio_url, os.sep.join([".", "resource", title, "audio"]), title)
    if len(title_url)>0:
        save_image(title_url, os.sep.join([".", "resource", title]), 'title')
    #print(result)
    with open(os.sep.join([".", 'resource', title, 'data.json']), 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=4)
    print("{} time tags extracted...".format(len(result.keys())))
    print("{} pictures saved...".format(count))
    
    
if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("Must specify gadio number... ")
        #update(str(108272))
    else:
        title=str(sys.argv[1])
        main(title)
