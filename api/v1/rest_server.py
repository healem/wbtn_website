#!../bin/python
import ConfigParser
from exceptions import NameError
import db.datastore
from db import datastore
import logging
from utils import loginit

from flask import Flask, Blueprint, jsonify, url_for, session, request

loginit.initLogging()
logger = logging.getLogger(__name__)

configFile = "/home/bythenum/keys/wbtn.cnf"
config = ConfigParser.ConfigParser()
config.read(configFile)
secret = config.get("app", "api_secret")

app = Flask(__name__)
app.logger.setLevel("DEBUG")
app.secret_key = secret

from rest.restplus import api, apiBlueprint
from rest.sample import sampleApi
from rest.auth.routes import authApi
from rest.user.routes import userApi
from rest.whiskey.routes import whiskeyApi
from rest.rating.routes import ratingApi
from rest import decorators

api.add_namespace(sampleApi)
api.add_namespace(authApi)
api.add_namespace(userApi)
api.add_namespace(whiskeyApi)
api.add_namespace(ratingApi)

app.register_blueprint(apiBlueprint)

app.logger.info("url_map before: %s", app.url_map)

#@app.before_request
#def debugOutput():
#    logger.info("URL root: %s and URL path: %s", request.url_root, request.full_path)
#    logger.info("Request url %s and args %s", request.url, request.values)
 
def main():
    logger.info("Starting app server")
    app.run(debug=False)
    
if __name__ == '__main__':
    main()
