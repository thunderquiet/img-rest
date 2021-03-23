

class Config( object ):
	RESIZE_NAME = "resize"


class DevelopmentConfig( Config ):
	IMG_STORE_PATH = "./img-store/"


class DockerProductionConfig( Config ):
	IMG_STORE_PATH = "/img-store/"



