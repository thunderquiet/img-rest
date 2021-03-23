
import uuid
import os
import sys
import zmq

from flask import Flask, request
from flask_restplus import Resource, Api, Namespace, reqparse
from werkzeug.datastructures import FileStorage


env = os.environ.get("APP_ENV", "Development") #assume dev env by default
app = Flask(__name__)
api = Api(app)

# import a single global config file that is shared between all services from the root of our project
sys.path.append(os.getcwd())
import config
app.config.from_object( 'config.'+env+'Config' )


@api.route('/resize/')
class ImageResize(Resource):
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('file', type=FileStorage, location='files',required=True)

    @api.expect(upload_parser)
    def post(self):
        guid = str( uuid.uuid4() )

        # get the file and save it to our location
        file = request.files['file']
        ext = os.path.splitext( file.filename )[1]
        file.save( os.path.join( app.config["IMG_STORE_PATH"], app.config["RESIZE_NAME"] + "_in_" + guid + ext ) )

        # now push the guid into zmq for processing and return


        return {"guid":guid}


@api.route('/resize/<string:guid>')
class ImageGetResized(Resource):
    def get(self, guid):
        return {"guid": guid}

@api.route('/resize/status/<string:guid>')
class ImageGetStatus(Resource):
    def get(self, guid):
        return {"guid": guid, "status": "working"}



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") #listen on all network interfaces

