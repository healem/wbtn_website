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

from rest.restplus import api, apiBlueprint
from rest.sample import sampleApi
from rest.auth.routes import authApi
from rest.user.routes import userApi
from rest import decorators

api.add_namespace(sampleApi)
api.add_namespace(authApi)
api.add_namespace(userApi)

app.register_blueprint(apiBlueprint)

#app.logger.info("url_map before: %s", app.url_map)

#@app.route('/')
#def hello_world():
#    return "Hello World!"
 
def main():
    logger.info("Starting app server")
    app.run(debug=False)
    
if __name__ == '__main__':
    main()
