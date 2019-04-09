import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

import crawler

def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']
    
    im = Image.open(path)
 
    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    
    try:
        while True:
            print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))
            
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('RGBA', im.size)
            
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')
 
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
 
def create_frame(image_name, title, content, size):
    print("Hello")
    #https://blog.csdn.net/wyx100/article/details/75579581

    # cv2读取图片
    img = cv2.imread(image_name) # 名称不能有汉字
    img = cv2.resize(img, (300,300))
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)

    frame = Image.new('RGB', size, color=(255,255,255))
    frame.paste(pilimg, (80, 80))
 
    # PIL图片上打印汉字
    draw = ImageDraw.Draw(frame) # 图片上打印

    font = ImageFont.truetype("msyh.ttc", 64, encoding="utf-8") 
    font2 = ImageFont.truetype("msyh.ttc", 30, encoding="utf-8") 
    # 参数1：字体文件路径，参数2：字体大小

    draw.text((450, 80), title, (0, 0, 0), font=font) 
    # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    draw.text((450, 180), content, (0, 0, 0), font=font2) 
    # PIL图片转cv2 图片
    cv2charimg = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    # cv2.imshow("图片", cv2charimg) # 汉字窗口标题显示乱码
    #cv2.imshow("photo", cv2charimg)
 
    #cv2.waitKey (0)
    #cv2.destroyAllWindows()
    return cv2charimg

 
def main():
    #processImage('673.gif')
    image_name = '.\\test\\3508.png'
    image_name2 = '.\\test\\3434.jpg'
    title = '中文标题'
    title2 = '中文标题2'
    content = '中文内容中文内容中文内容中文内容中文内容中文内容\n中文内容中文内容中文内容中文内容中文内容中文内容\n中文内容中文内容中文内容中文内容'
    content2 = '中文内容中文内容中文内容中文内容中文内容中文内容2\n中文内容中文内容中文内容中文内容中文内容中文内容\n中文内容中文内容中文内容中文内容'
    size = (1280, 720)
    frame = create_frame(image_name, title, content, size)
    frame2 = create_frame(image_name2, title2, content2, size)

    width = 1280
    height = 720
    FPS = 20
    seconds = 10
    radius = 150

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./circle_noise.avi', fourcc, float(FPS), (width, height))

    for i in range(10):
        print(i)
        video.write(frame)
    for i in range(20):
        print(i)
        video.write(frame2)
    for i in range(20):
        print(i)
        video.write(frame)
    for i in range(20):
        print(i)
        video.write(frame2)
    for i in range(20):
        print(i)
        video.write(frame)
    for i in range(20):
        print(i)
        video.write(frame2)

    video.release()

    
 
if __name__ == "__main__":
    main()