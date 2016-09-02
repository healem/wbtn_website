#!../bin/python
import ConfigParser
import db.datastore
import utils.loginit
import social.interface
import social.social_types
from db import datastore
from utils import loginit
from cachetools import LRUCache

from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

loginit.initLogging()
dbm = datastore.DbManager(testMode=True)

@app.route('/')
def hello_world():
    return "Hello World!"

##################
## Authorization
##################
class Users(Resource):
    def __init__(self, err):
        super(Users, self).__init__()
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        self.userCache = LRUCache(maxsize=500, missing=getUser)
        
    def getUser(self, token):
        ## Verify the user is authenticated by facebook
        auth = Social.get_provider(SocialType.provider)
        if auth.verify(token):
            ## Great!  Now lets see if they are registered with us
            
            user = dbm.getUserByEmail(email)
        
        
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('provider', type = str, location = 'json')
            parse.add_argument('token', type = str, location = 'json')
            args = parser.parse_args()
            
            provider = args['provider']
            token = args['token']
            
            auth = Social.get_provider(SocialType.provider)
            
            #see if user is in cache
            #verify user
            #cache token
            #get email, make sure local user exists, if not - create
            if auth.verify(token):
                user = dbm.getUserByEmail


# @app.route('/authorize/<provider>')
# def oauth_authorize(provider):
#     oauth = Social.get_provider(provider)
#     return oauth.authorize()
# 
# @app.route('/callback/<provider>')
# def oauth_callback(provider):
#     oauth = Social.get_provider(provider)
#     socialId, email, firstName, lastName = oauth.callback()
#     if email is None:
#         return None
#     user = dbm.getUserByEmail(email)
#     #if not user:
#     #    dbm.addNormalUser(email=testEmail, facebookId=socialId, firstName=firstName, lastName=lastName)
#     #    user = dbm.getUserByEmail(email)
        
 #   return user

if __name__ == '__main__':
    app.run(debug=True)

