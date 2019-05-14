import argparse
import json
import os
import re
import urllib

from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import Image, ImageDraw, ImageFont


def find_image_suffix(image_name:str):
    file_suffix = re.match(".*(\..*)", image_name).group(1)
    return file_suffix

def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

def is_non_start(string):
    return string in """!%),.:;>?]}¢¨°·ˇˉ―‖’”…‰′″›℃∶、。〃〉》」』】〕〗〞︶︺︾﹀﹄﹚﹜﹞！＂％＇），．：；？］｀｜｝～￠"""

def is_non_end(string):
    return string in """$([{£¥·‘“〈《「『【〔〖〝﹙﹛﹝＄（．［｛￡￥"""

def is_character(string:str):
    return ((not is_alnum(string)) and (not is_non_start(string)) and (not is_non_end(string)))

def is_alnum(string:str):
    return string in "1234567890abcdefghijklmnopqrstuvwxyzßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþąćĉčďęěĝğĥıĵłńňœřśŝşšťŭůźżžABCDEFGHIJKLMNOPQRSTUVWXYZSSÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞĄĆĈČĎĘĚĜĞĤIĴŁŃŇŒŘŚŜŞŠŤŬŮŹŻŽ"

def convert_to_string(string:str):
    str_code = urllib.parse.unquote(string)
    return str_code

def seconds_to_time(seconds:int):
    try:
        seconds = int(seconds)
        if(seconds<0):
            return "-00:01"
    except:
        return "-00:01"

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if(h==0):
        return "%02d:%02d"%(m,s)
    else:
        return "%d:%02d:%02d" % (h, m, s)

def extract_bilibili_video_id(link:str):
    "https://www.bilibili.com/video/av48185229?from=search&seid=15830345666680669730"
    if "bilibili.com" in link:
        try:
            video_id = re.match(".*\/(.v[0-9]*)", link).group(1)
            return video_id
        except Exception as e:
            print("Not a valid video url", link)
            return link
    else:
        print("Not a valid bilibili url", link)
        return link
        

class Wrapper(object):
    def __init__(self, font:ImageFont):
        self.font = font
        self.tokens = list()

    def wrap_string(self, string:str, width):
        self.tokenize_string(string)
        result = str()
        temp_string = str()
        length = 0
        for word in self.tokens:
            word_length = self.font.getsize(word)[0]
            if(length+word_length>width):
                result+=temp_string
                result+="\n"
                temp_string = word
                length = word_length
            else:
                temp_string+=word
                length+=word_length
        result+=temp_string
        #result = result.replace("\\n ", "\\n", 100)
        return result
    
    def tokenize_string(self, string:str):
        self.tokens.clear()
        s = str()
        string = string.replace("\n","",100)
        for character in string:
            if(len(s)==0):
                s=character
            else:
                last_character = s[len(s)-1]
                #print(last_character)
                if(is_alnum(character)):
                    if(is_alnum(last_character)):
                        s+=character
                    elif(is_non_end(last_character)):
                        s+=character
                    else:
                        self.tokens.append(s)
                        s=character
                elif(is_character(character)):
                    if(is_non_end(last_character)):
                        s+=character
                    else:
                        self.tokens.append(s)
                        s=character
                elif(is_non_start(character)):
                    s+=character
                else:
                    self.tokens.append(s)
                    s = character

        #print(result)
        if(len(s)!=0):
            self.tokens.append(s)
        return self.tokens

def load_data(title:str):
    title = str(title)
    file_dir = os.sep.join([".", "resource", title, "data.json"])
    result = {}
    try:
        with open(file_dir, "r", encoding='utf-8') as f:
            result = json.loads(f.read())
            return result
    except Exception as e:
        print("Error: ", e)
        return result

def extract_links(result:dict, title:str):
    with open(os.sep.join(['.', "output", title+ ".txt"]), 'w+', encoding='utf-8') as links:
        length = 0
        last = ""
        for key in result.keys():
            if(len(result[key]['link'])>0):
                header = result[key]['header']
                if(key==0):
                    key+=1
                time_string = seconds_to_time(key+config['open_offset'])
                url = result[key]['link']
                url = convert_to_string(url)
                if("bilibili" in url):
                    url = extract_bilibili_video_id(url)
                if(url==last):
                    continue
                else:
                    last = url
                line = time_string+" "+header+" "+url+"\n"
                length+=len(line)
                if(length>950): # Bilibili comment length 1000
                    links.write("\n\n")
                    length=0
                links.writelines(line)
    links.close()


if __name__ == "__main__":
    #print(find_image_suffix("Hello.jpg"))
    line = input()
    font = ImageFont.truetype("msyh.ttc", 40, encoding="utf-8") 
    wrapper=Wrapper(font)
    strin  = wrapper.wrap_string(line, width= 600)
    print(wrapper.tokens)
    print(strin)
    #print(load_data(108639))
    print(font.getsize_multiline("Hello"))
    print(font.getsize_multiline("Hello\nHello\nHello"))
    print(extract_bilibili_video_id("https://www.bilibili.com/video/av48185229?from=search&seid=15830345666680669730"))
    print(convert_to_string("http://www.wikiwand.com/zh-sg/%E5%B8%9D%E5%9C%8B%E9%98%B2%E8%A1%9B%E8%BB%8D_(%E6%88%B0%E9%8E%9A40000)#/%E8%B6%85%E9%87%8D%E5%9E%8B%E5%9D%A6%E5%85%8B"))