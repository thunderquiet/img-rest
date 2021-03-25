

import os
import json
import time
from PIL import Image
import sys

import zmq

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/../" )
import config


class ImgEngine():
	
	def __init__(self, env):
		self.config = getattr(config, env+"Config")

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.DEALER)
		self.socket.bind("tcp://*:5555")
		print("ZMQ Ready...")


	def run( self ):
		while True:
		    #  Wait for next request from client
		    msg = json.loads( self.socket.recv().decode() )
		    print("Received request:" + str(msg) )

		    # load the image, resize it and save back to new location
		    img = self._load_img( msg["guid"], msg["cmd"], "in" )
		    thumb = self._resize( img, msg["width"], msg["height"] )
		    self._save_img( thumb, msg["guid"], msg["cmd"], "out" )


	
	def _resize( self, img, width, height ):
		thumb = img.resize( (width,height) )
		return thumb


	def _load_img( self, guid, cmd, step ):
		filepath = os.path.join( self.config.IMG_STORE_PATH, cmd + "_"+step+"_" + guid + ".jpg" )
		img = Image.open( filepath )
		return img


	def _save_img( self, img, guid, cmd, step ):
		# assume "jpg extension"
		filepath = os.path.join( self.config.IMG_STORE_PATH, cmd + "_"+step+"_" + guid + ".jpg" )
		img.save( filepath )



def main():
	env = os.environ.get("APP_ENV", "Development") #assume dev env by default
	eng = ImgEngine( env )
	eng.run()


if __name__ == '__main__':
    main()
