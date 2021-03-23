
import uuid

from flask import Flask, request
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

@api.route('/resize/')
class ImageResize(Resource):
    def post(self):
        return {"guid": uuid.uuid4() }
   
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

