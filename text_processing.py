import re

def find_image_suffix(image_name:str):
    file_suffix = re.match(".*(\..*)", image_name).group(1)
    return file_suffix

if __name__ == "__main__":
    print(find_image_suffix("Hello.jpg"))
