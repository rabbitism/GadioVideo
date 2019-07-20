import json
import os
import re
import urllib

from PIL import Image, ImageDraw, ImageFont
from gadio.configs.config import config


def find_image_suffix(image_name: str):
    print(image_name)
    try:
        file_suffix = re.match(".*(\..*)", image_name).group(1)
        return file_suffix
    except:
        print("Invalid picture id")
        return ""

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
                time_string = seconds_to_time((1 if key==0 else key)+config['open_offset'])
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
                length=len(line)
    links.close()

def extract_headers(result:dict, title:str):
    with open(os.sep.join(['.', "output", title+ "_headers.txt"]), 'w+', encoding='utf-8') as links:
        length = 0
        last = ""
        for key in result.keys():
            if(len(result[key]['header'])>0):
                header = result[key]['header']
                time_string = seconds_to_time((1 if key==0 else key)+config['open_offset'])
                line = time_string+" "+header+"⭐"
                length+=len(line)
                if(length>950): # Bilibili comment length 1000
                    links.write("\n\n")
                    length=len(line)
                links.writelines(line)
    links.close()