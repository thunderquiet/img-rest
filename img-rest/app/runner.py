
import uuid
import json
import os
import sys
import zmq as ZMQ

from flask import Flask, request, send_file
from flask_restplus import Resource, Api, Namespace, reqparse
from werkzeug.datastructures import FileStorage

from utils import create_app



env = os.environ.get("APP_ENV", "Development") #assume dev env by default
print( env )
app, api, zmq = create_app( env )


@api.route('/resize/')
class ImageResize(Resource):
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('file', type=FileStorage, location='files',required=False)

    @api.expect(upload_parser)
    def post(self):
        guid = str( uuid.uuid4() )

        # get the file and save it to our location
        file = request.files['file']
        file.save( os.path.join( app.config["IMG_STORE_PATH"], app.config["RESIZE_NAME"] + "_in_" + guid + ".jpg" ) )

        # now push the guid into zmq for processing and return
        cmd = {"cmd":"resize", "width":100, "height":100, "guid":guid}
        zmq.send( bytes(json.dumps( cmd ), "utf-8") )

        return {"guid":guid}


# TODO - we should be doing validation that input string is a valid guid
@api.route('/resize/<string:guid>')
class ImageGetResized(Resource):
    def get(self, guid):
        path = os.path.join( app.config["IMG_STORE_PATH_GET"], app.config["RESIZE_NAME"] + "_out_" + guid + ".jpg" )
        return send_file( path )


@api.route('/resize/status/<string:guid>')
class ImageGetStatus(Resource):
    def get(self, guid):
        path = os.path.join( app.config["IMG_STORE_PATH"], app.config["RESIZE_NAME"] + "_out_" + guid + ".jpg" )
        status = "processing"
        if os.path.isfile( path ):
            status = "complete"
        return {"guid": guid, "status": status}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") #listen on all network interfaces

