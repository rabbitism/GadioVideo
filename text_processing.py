import re
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import Image, ImageDraw, ImageFont


def find_image_suffix(image_name:str):
    file_suffix = re.match(".*(\..*)", image_name).group(1)
    return file_suffix

def is_chinese(uchar):
    if uchar >= u'/u4e00' and uchar<=u'/u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    if uchar >= u'/u0030' and uchar<=u'/u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    if (uchar >= u'/u0041' and uchar<=u'/u005a') or (uchar >= u'/u0061' and uchar<=u'/u007a'):
         return True
    else:
        return False

def is_other(uchar):
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

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
            if((length+actual_length)>width and (actual_word not in ["，。？！）》"])):
                result+=temp_string
                result+="\n"
                temp_string = actual_word
                length = actual_length
            else:
                temp_string+=actual_word
                length+=actual_length
        #print(result)
        return result+temp_string

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
                    result.append(" "+str(char)+" ")
            temp.append(" ")
            result.append("".join(temp))
            temp.clear()
        self.tokens = "".join(result).split()
        return self.tokens


if __name__ == "__main__":
    print(find_image_suffix("Hello.jpg"))
    line = input()
    font = ImageFont.truetype("msyh.ttc", 30, encoding="utf-8") 
    #print(font.getsize("Hello"))
    #print(font.getsize("您好"))
    #print(font.getsize("Google"))
    #print(font.getsize("Hello 您好"))
    wrapper=Wrapper(font)
    #tokens = wrapper.tokenize_string(line)
    #for word in tokens:
        #print(len(word), end=' ')
    #print(is_alpha("是"))
    #for char in "是不是 sbs":
    #    print(is_alpha(char))
    strin  = wrapper.wrap_string(line, width= 600, height=200, width2 = 1000)
    print(strin)
    
    
