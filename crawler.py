import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.request

import text_processing

def crawler(number):
    """
    Get timeline and corresponding contents from Gcores webiste.
    returns:
    result: a dictionary if this format: {10:{'header':'标题', 'content':'内容', 'image_url':'https://......123.jpg','image_suffix':'.jpg'}}
    audio_line: url to audio file: 'https://......123.mp3'
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

    audio_line = soup.find("p", {'class': 'story_actions'}).contents[1]["href"]

    return result, audio_line

def save_image(image_url, image_dir, image_name):
    try:
        if not os.path.exists(image_dir):
            print("Folder", image_dir, 'does not exist. Creating...')
            os.makedirs(image_dir)
        file_suffix = re.match(".*(\..*)", image_url).group(1)
        #print(file_suffix)
        print("Saving image to", image_name+file_suffix)
        with open(image_dir+os.sep+image_name+file_suffix, 'wb') as f:
            f.write(requests.get(image_url).content)
    except Exception as e:
        print("Error", e)

def save_audio(audio_url, audio_dir, audio_name):
    print("Saving Audio...")
    try:
        if not os.path.exists(audio_dir):
            print("Folder", audio_dir, "does not exist. Creating...")
            os.makedirs(audio_dir)
        print("Saving audio to", audio_name + ".mp3")
        r = urllib.request.urlretrieve(audio_url, audio_dir + os.sep + audio_name + ".mp3")
        ##with open(audio_dir + os.sep + audio_name + ".mp3") as code:
        #   code.write(r.content)
    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    title = str(108272)
    result, audio_url = crawler(title)
    save_audio(audio_url, ".\\test", "test")
    #for key in result.keys():
    #    image_name = key
    #    image_url = result[key]['image_url']
    #    image_dir = os.sep.join([".", "resource", title])
    #    #save_image(image_url, image_dir, image_name)