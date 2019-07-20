import os

config = {
    'fps':2,
    'width':1920,
    'height':1080,
    'title_font_size': 53,
    'content_font_size': 36,
    'gcores_title_color': (255,255,255,246),
    'gcores_content_color': (255,255,255,205),
    'background_color':"#FFFFFF",
    'title_font': os.sep.join([os.curdir, 'gadio', 'utils', 'PingFang-Heavy.ttf']),
    'content_font': os.sep.join([os.curdir, 'gadio', 'utils', 'PingFang-Medium.ttf']),
    'gcores_logo_name': os.sep.join([os.curdir, 'gadio', 'utils', 'gcores.png']),
    'gcores_qr_name': os.sep.join([os.curdir, 'gadio', 'utils', 'qr.png']),
    'test':False,
    'open_offset':0
}