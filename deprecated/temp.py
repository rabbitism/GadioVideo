def is_non_start(string):
    return string in """!%),.:;>?]}¢¨°·ˇˉ―‖’”…‰′″›℃∶、。〃〉》」』】〕〗〞︶︺︾﹀﹄﹚﹜﹞！＂％＇），．：；？］｀｜｝～￠"""

def is_non_end(string):
    return string in """$([{£¥·‘“〈《「『【〔〖〝﹙﹛﹝＄（．［｛￡￥"""

def is_character(string:str):
    return ((not is_alnum(string)) and (not is_non_start(string)) and (not is_non_end(string)))

def is_alnum(string:str):
    return string in "abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def tokenize_string(string:str):
    result = list()
    s = str()
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
                    result.append(s)
                    s=character
            elif(is_character(character)):
                if(is_non_end(last_character)):
                    s+=character
                else:
                    result.append(s)
                    s=character
            elif(is_non_start(character)):
                s+=character
            else:
                result.append(s)
                s = character   
    #print(result)
    return result


if __name__ == "__main__":
    strin = input()
    tokens = tokenize_string(strin)
    for character in tokens:
        print(character)
    #print("是".isalnum())