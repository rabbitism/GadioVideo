import json
import os
import re
import sys
import urllib.request

import requests
from bs4 import BeautifulSoup

import text_processing
from config import config


def crawler(number):
    """Get timeline and corresponding contents from Gcores webiste.
    
    Arguments:
        number {str} -- gadio number
    
    Returns:
        dict, str -- a dictionary in this format: {10:{'header':'标题', 'content':'内容', 'image_url':'https://......123.jpg','image_suffix':'.jpg'}}
    """

    # Get source code
    url = "https://www.gcores.com/radios/"+str(number)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    b = soup.findAll("div", {'class':['row']})
    result = dict()
    for line in b:
        # Get lines with image information
        image_div = line.find('div', {'class':'col-xs-5'})

        if(image_div is not None):
            image_line = image_div.find('img')

        # Get lines with text information
        header = line.find('div', {'class':'col-xs-7'})
        if(header is not None):
            header_line = header.find('h1').contents[0].strip()
            content_line = header.find('p').contents[0].strip()
            time = int(header.find('h1').contents[1]['data-at'])
            image_suffix = text_processing.find_image_suffix(image_line['src'])
            result[time] = {'header':header_line, 'content':content_line, 'image_url':image_line['src'], 'image_suffix':image_suffix}
    try:
        audio_line = soup.find("p", {'class': 'story_actions'}).contents[1]["href"]
    except:
        audio_line = ""
    return result, audio_line

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
    result, audio_url = crawler(title)
    test = config['test']
    count = 0
    for key in result.keys():
        image_name = str(key)
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        count+=save_image(image_url, image_dir, image_name)

    save_audio(audio_url, os.sep.join([".", "resource", title, "audio"]), title)
    print(result)
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
