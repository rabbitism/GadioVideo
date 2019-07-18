import json
import os
import re
import urllib

from PIL import Image, ImageDraw, ImageFont

from gadio.configs.config import config
from gadio.text.text import *

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