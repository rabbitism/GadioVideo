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
    #crawler()

    from PIL import Image, ImageDraw, ImageFont
    import cv2
    import numpy as np
 
    # cv2读取图片
    img = cv2.imread('.\\test\\3508.png') # 名称不能有汉字
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)
 
    # PIL图片上打印汉字
    draw = ImageDraw.Draw(pilimg) # 图片上打印
    font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8") # 参数1：字体文件路径，参数2：字体大小
    draw.text((0, 0), "Hi,我是兔基", (255, 0, 0), font=font) # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
 
    # PIL图片转cv2 图片
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    # cv2.imshow("图片", cv2charimg) # 汉字窗口标题显示乱码
    cv2.imshow("photo", cv2charimg)
 
    cv2.waitKey (0)
    cv2.destroyAllWindows()

