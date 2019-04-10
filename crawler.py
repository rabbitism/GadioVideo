import requests
from bs4 import BeautifulSoup
import os
import re

def crawler(number):
    url = "https://www.gcores.com/radios/"+str(number)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    b = soup.findAll("div", {'class':['row']})
    result = dict()
    for line in b:
        image_div = line.find('div', {'class':'col-xs-5'})
        #print(image_div)
        if(image_div is not None):
            image_line = image_div.find('img')

        header = line.find('div', {'class':'col-xs-7'})
        if(header is not None):
            header_line = header.find('h1').contents[0].strip()
            content_line = header.find('p').contents[0].strip()
            time = int(header.find('h1').contents[1]['data-at'])

        result[time] = {'header':header_line, 'content':content_line, 'image_url':image_line['src']}
    #print(result)
    return result

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

if __name__ == "__main__":
    title = str(108272)
    result = crawler(title)
    for key in result.keys():
        image_name = key
        image_url = result[key]['image_url']
        image_dir = os.sep.join([".", "resource", title])
        save_image(image_url, image_dir, image_name)