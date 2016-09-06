#!../bin/python
import ConfigParser
from exceptions import NameError
import db.datastore
from db import datastore
from utils import loginit

from flask import Flask, jsonify
from rest import api

app = Flask(__name__)
api.init_app(app)

loginit.initLogging()
logger = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"
 
def main():
    logger.info("Starting app server")
    app.run(debug=False)
    
if __name__ == '__main__':
    main()

