import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

import requests
from bs4 import BeautifulSoup

def create_video():
    width = 1280
    height = 720
    FPS = 10
    seconds = 10
    radius = 150
    paint_h = int(height/2)

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./circle_noise.avi', fourcc, float(FPS), (width, height))

    for paint_x in range(-radius, width+radius, 6):
        print(paint_x)
        frame = np.random.randint(0, 256, 
                              (height, width, 3), 
                              dtype=np.uint8)
        cv2.circle(frame, (paint_x, paint_h), radius, (0, 0, 0), -1)
        video.write(frame)

    video.release()


def crawler():
    url = "https://www.gcores.com/radios/108272"
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
            time = header.find('h1').contents[1]['data-at']
        #print(time)
        #print(header_line)
        #print(content_line)
        #print(image_line['src'])
        #if('col-xs-5' in line['class']):
            #print(line)
        #    image_line =line.findAll('img')
        #    image_url = image_line[0]['src']
        #else:
        #    header_line = line.find('h1')
        #    header = header_line.contents[0].strip()
        #    content_line = line.find('p')
        #    content = content_line.contents[0].strip()
        #    time = header_line.contents[1]['data-at']
        #    print(time)
        #    print(header)
        #    print(content)
        result[time] = {'header':header_line, 'content':content_line, 'image_url':image_line['src']}
    print(result)
    return result
            
def crawler2():
    url = "https://www.gcores.com/radios/108272"
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    script = soup.findAll('script', attrs={'type':'text/javascript'})
    print(script)
            


if __name__ == "__main__":
    import pip
    from pip._internal.utils.misc import get_installed_distributions
    from subprocess import call
 
    for dist in get_installed_distributions():
    # 执行后，pip默认为Python3版本
    # 双版本下需要更新Python2版本的包，使用py2运行，并将pip修改成pip2
        call("pip install --upgrade " + dist.project_name+" -i https://pypi.mirrors.ustc.edu.cn/simple", shell=True)
