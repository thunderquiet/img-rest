

class Config( object ):
	RESIZE_NAME = "resize"
	ZMQ_PORT = 5555

# local dev
class DevelopmentConfig( Config ):
	IMG_STORE_PATH = "./img-store/"
	ZMQ_HOST = "localhost"

# unit tests
class TestConfig( Config ):
	IMG_STORE_PATH = "../img-store/"
	ZMQ_HOST = "localhost"

# production deployed to docker
class DockerProductionConfig( Config ):
	IMG_STORE_PATH = "/img-store/"
	ZMQ_HOST = "engine"


