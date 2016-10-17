#!../../../bin/python
import logging
import json
from flask import session
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from db import datastore
from ..restplus import api
from ..decorators import require_token, require_admin
from ..user_cache import userCache
from helpers import updateUser

logger = logging.getLogger("User-routes")
userApi = Namespace('user', description='User related operations')

user = userApi.model('User', {
    'userId': fields.String(required=True, description='The user identifier'),
    'email': fields.String(required=True, description='The email address of the user'),
    'firstName': fields.String(required=False, description='User first name'),
    'lastName': fields.String(required=False, description='User last name'),
    'createdTime': fields.DateTime(required=True, description='When the user was created'),
    'lastUpdatedTime': fields.DateTime(required=True, description='The last time the user profile was updated'),
    'userRater': fields.Boolean(required=True, description='User has permission to rate whiskies'),
    'blogWriter': fields.Boolean(required=True, description='User has permission to create blog posts'),
    'collegeRater': fields.Boolean(required=True, description='User has permission to create advanced ratings'),
    'whiskeyAdmin': fields.Boolean(required=True, description='User is an admin'),
    'currentPage': fields.Integer(required=False, description='Current page for multi-page query'),
    'itemsPerPage': fields.Integer(required=False, description='The numbers of items to return per page of a multi-page query'),
})

dbm = datastore.DbManager(testMode=False)

getParser = userApi.parser()
getParser.add_argument('email', type=str, required=True, help='The user email address')

postParser = userApi.parser()
postParser.add_argument('email', type=str, required=True, help='The user email address')
postParser.add_argument('userId', type=str, required=False, help='The user identifier')
postParser.add_argument('firstname', type=str, required=False, help='User first name')
postParser.add_argument('lastname', type=str, required=False, help='User last name')
postParser.add_argument('userRater', type=bool, required=False, help='User has permission to rate whiskies')
postParser.add_argument('blogWriter', type=bool, required=False, help='User has permission to create blog posts')
postParser.add_argument('collegeRater', type=bool, required=False, help='User has permission to create advanced ratings')
postParser.add_argument('whiskeyAdmin', type=bool, required=False, help='The user is an admin')
postParser.add_argument('dumpCache', type=bool, required=False, help='Flush the user cache')

getAllParser = userApi.parser()
getAllParser.add_argument('currentPage', type=int, required=True, default=1, help='Current page of the query, count starts at 1')
getAllParser.add_argument('itemsPerPage', type=int, required=True, default=20, help='Number of items returned per page, max=100')

@api.route('/allusers')
class WBTNUsers(Resource):
    @require_token
    @require_admin
    @api.expect(getAllParser, True)
    def get(self):
        #logger.debug("Incoming request for all users")
        args = getAllParser.parse_args()
        #logger.debug("Getting all users with args: %s", args)
        allUsers = dbm.getAllUsers(args['currentPage'], args['itemsPerPage'])
        #logger.debug("Returning allUsers: %s", allUsers)
        return allUsers

@api.route('/user')
class WBTNUser(Resource):
    @require_token
    @require_admin
    @api.expect(getParser)
    def get(self):
        args = getParser.parse_args()
        return json.dumps(getUserByEmail(args['email']).__dict__)
    
    @require_token
    @require_admin
    @api.expect(postParser)
    def post(self):
        args = postParser.parse_args()
        return updateUser(args)
         
@api.route('/me')
class WBTNMe(Resource):
    @require_token
    def get(self):
        # Because the session must have a token, the user will be in the cache
        return json.dumps(userCache.get(session['api_session_token']).__dict__)
    
    @require_token
    def put(self):
        # Flush my session from cache
        logger.debug("Attempting to flush session from cache")
        result = userCache.pop(session['api_session_token'])
        if result is None:
            logger.debug("Session not in cache - nothing to remove")
            
        user = userCache.get(session['api_session_token'])
        if user is not None:
            logger.warn("User not removed from cache")
            abort(500, reason="FLUSH_FAILED")
            
        return 200
    
def getUserByEmail(email):
    return dbm.getUserByEmail(email)

    
