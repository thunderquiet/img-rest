

import os
from PIL import Image
import sys
import unittest

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/app")
from app.runner import ImgEngine


class Tests(unittest.TestCase):

    def test_resize_correct(self):
        eng = ImgEngine("Test")
        img = Image.new( "RGB", (1000, 1000) )
        thumb = eng._resize( img, 100, 100 )
        
        self.assertEqual( thumb.width, 100 )


if __name__ == '__main__':
    unittest.main()

