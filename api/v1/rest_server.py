#!../bin/python
import ConfigParser
from exceptions import NameError
import db.datastore
from db import datastore
import logging
from utils import loginit

from flask import Flask, Blueprint, jsonify, url_for, session

loginit.initLogging()
logger = logging.getLogger(__name__)

configFile = "/home/bythenum/keys/wbtn.cnf"
config = ConfigParser.ConfigParser()
config.read(configFile)
secret = config.get("app", "api_secret")

app = Flask(__name__)
app.secret_key = secret

from rest.restplus import api
from rest.sample import api as sample_api
from rest.auth import api as auth_api
from rest.user import api as user_api
from rest import decorators

blueprint = Blueprint('api', __name__)

api.add_namespace(sample_api)
api.add_namespace(auth_api)
api.add_namespace(user_api)

app.register_blueprint(blueprint)

#app.logger.info("url_map before: %s", app.url_map)

#@app.route('/')
#def hello_world():
#    return "Hello World!"
 
def main():
    logger.info("Starting app server")
    app.run(debug=False)
    
if __name__ == '__main__':
    main()
