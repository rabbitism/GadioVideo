import unittest
import sys
import os
import json

from gadio.text import text as text
from gadio.models.radio import Radio

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

        import gadio.configs
        import gadio.crawlers
        import gadio.media
        import gadio.models
        import gadio.text

class TestText(unittest.TestCase):
    def test_find_suffix(self):
        self.assertEqual('.jpg', text.find_image_suffix('1.jpg'))
        self.assertEqual('.jpg', text.find_image_suffix('1.1.jpg'))
        self.assertEqual('', text.find_image_suffix(None))
    
    def test_is_alpha(self):
        self.assertTrue(text.is_alpha("Hello"))
        self.assertFalse(text.is_alpha("12Hello"))
        self.assertFalse(text.is_alpha("是的"))
    
    def test_is_alnum(self):
        self.assertTrue(text.is_alnum('A'))
        self.assertFalse(text.is_alnum('.'))
        self.assertTrue(text.is_alnum('1'))
        self.assertFalse(text.is_alnum('是'))

    def test_seconds_to_time(self):
        self.assertEqual("00:00", text.seconds_to_time(0))
        self.assertEqual("01:00", text.seconds_to_time(60))
        self.assertEqual("-00:01", text.seconds_to_time(-1))
        self.assertEqual("-00:01", text.seconds_to_time("a"))
        self.assertEqual("1:00:01", text.seconds_to_time(3601))
        self.assertEqual("2:46:40", text.seconds_to_time(10000))

"""
class RadioTest(unittest.TestCase):
    def test_radio(self):
        parsed_json = object
        with open(os.sep.join(['.', 'test', 'radio.json']), 'r', encoding='utf-8') as f:
            parsed_json = json.loads(f.read())
        radio = Radio.load_from_json(parsed_json)
        self.assertEqual('112725', radio.radio_id)
        self.assertEqual('我们为何如此喜爱Metroidvania游戏', radio.title)
        self.assertEqual(81, len(radio.timeline))
        self.assertEqual(4, len(radio.users))
        if (0 in radio.timeline.keys()):
            self.assertTrue(len(radio.timestamps) == len(radio.timeline) + 1)
        else:
            self.assertTrue(len(radio.timestamps) == len(radio.timeline) + 2)
            """

if __name__ == "__main__":
    unittest.main()
