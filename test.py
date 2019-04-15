import unittest

import text_processing

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