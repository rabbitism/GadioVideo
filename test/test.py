import unittest

import text_processing
import simple
import complex
import animated

class TestDependency(unittest.TestCase):
    def test_dependency(self):
        import math
        import os
        import sys

        import cv2
        import numpy as np
        from cv2 import VideoWriter, VideoWriter_fourcc
        import moviepy.editor
        from PIL import Image, ImageDraw, ImageFont

        import crawler
        import image_processing
        import text_processing
        import video_processing
        from config import config

class TestText(unittest.TestCase):
    def test_find_suffix(self):
        self.assertEqual('.jpg', text_processing.find_image_suffix('1.jpg'))
        self.assertEqual('.jpg', text_processing.find_image_suffix('1.1.jpg'))
    
    def test_is_alpha(self):
        self.assertTrue(text_processing.is_alpha("Hello"))
        self.assertFalse(text_processing.is_alpha("12Hello"))
        self.assertFalse(text_processing.is_alpha("是的"))
    
    def test_is_alnum(self):
        self.assertTrue(text_processing.is_alnum('A'))
        self.assertFalse(text_processing.is_alnum('.'))
        self.assertTrue(text_processing.is_alnum('1'))
        self.assertFalse(text_processing.is_alnum('是'))
    
    def test_bilibili_video_id(self):
        self.assertEqual('av48185229', text_processing.extract_bilibili_video_id("https://www.bilibili.com/video/av48185229?from=search&seid=15830345666680669730"))
        self.assertEqual('av48185229', text_processing.extract_bilibili_video_id("https://www.bilibili.com/video/av48185229/"))
        self.assertEqual('av48185229', text_processing.extract_bilibili_video_id("https://www.bilibili.com/video/av48185229"))
        self.assertEqual('av48185229', text_processing.extract_bilibili_video_id("www.bilibili.com/video/av48185229"))
        self.assertEqual('https://www.baidu.com/video/av48185229', text_processing.extract_bilibili_video_id("https://www.baidu.com/video/av48185229"))
        self.assertEqual('https://www.gcores.com/radios/108272', text_processing.extract_bilibili_video_id("https://www.gcores.com/radios/108272"))

    def test_seconds_to_time(self):
        self.assertEqual("00:00", text_processing.seconds_to_time(0))
        self.assertEqual("01:00", text_processing.seconds_to_time(60))
        self.assertEqual("-00:01", text_processing.seconds_to_time(-1))
        self.assertEqual("-00:01", text_processing.seconds_to_time("a"))
        self.assertEqual("1:00:01", text_processing.seconds_to_time(3601))
        self.assertEqual("2:46:40", text_processing.seconds_to_time(10000))

if __name__ == "__main__":
    unittest.main()