

import os
import sys
import zmq

from flask import Flask, current_app
from flask_restplus import Api



def create_app( env ):
    app = Flask(__name__)
    # import a single global config file that is shared between all services from the root of our project
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd() + "/../" )
    import config
    app.config.from_object( 'config.'+env+'Config' )

    api = Api(app)

    # open connection to our ZMQ engine
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)#this puts the msg queue into async mode - https://zeromq.org/socket-api/
    socket.connect("tcp://" + app.config["ZMQ_HOST"] + ":" + str(app.config["ZMQ_PORT"]) )
    return (app, api, socket)



