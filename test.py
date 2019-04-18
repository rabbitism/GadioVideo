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

if __name__ == "__main__":
    unittest.main()