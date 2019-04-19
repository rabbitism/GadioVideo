import re
import os
import json
import argparse

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