import re
import os
import json

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
            actual_word = word if len(word)==1 else (word+" ")
            actual_length = self.font.getsize(actual_word)[0]
            #if((length+actual_length)>width and (actual_word not in ["，。？！）》"])):
            if((length+actual_length)>width):
                result+=temp_string
                result+="\n"
                temp_string = actual_word
                length = actual_length
            else:
                if(len(actual_word)==1):
                    temp_string =temp_string.rstrip()
                temp_string+=actual_word
                length+=actual_length
        #print(result)
        result+=temp_string
        for char in "，。？！；：》>]}】）)、":
             result = result.replace("\n"+char, char+"\n", 20)
        for char in "《<[{【（(":
             result = result.replace(char+"\n", "\n"+char, 20)
        
        return result

    def tokenize_string(self, string:str):
        self.tokens.clear()
        words = string.split()
        result = list()
        temp = list()
        for word in words:
            for char in word:
                if(is_alpha(char) or char.isdigit()):
                    temp.append(char)
                else:
                    result.append("".join(temp))
                    temp.clear()
                    result.append(" "+str(char))
            temp.append(" ")
            result.append("".join(temp))
            temp.clear()
        self.tokens = "".join(result).split()
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
    #line = input()
    #font = ImageFont.truetype("msyh.ttc", 30, encoding="utf-8") 
    #wrapper=Wrapper(font)
    #strin  = wrapper.wrap_string(line, width= 600, height=200, width2 = 1000)
    #print(strin)
    print(load_data(108639))