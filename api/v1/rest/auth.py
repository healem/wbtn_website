#!../../bin/python
import logging
from flask_restplus import Resource, Namespace, reqparse
from cachetools import TTLCache

api = Namespace('auth', description='User authentication and authorization related operations')

auth = api.model('Auth', {
    'token': fields.String(required=True, description='The user session token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
})

@api.route('/')
class Auth(Resource):
    
    userCache = TTLCache(maxsize=500, ttl=3600, missing=getUser)
    dbm = datastore.DbManager(testMode=False)
    
    def __init__(self, err):
        super(Users, self).__init__()
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        self.provider = None      
        
    @api.expect(auth)
    @api.param('provider', 'the provider of the token', 'formData')
    @api.param('token', 'the access token from the provider', 'formData')
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('provider', type = str, location = 'json')
            parse.add_argument('token', type = str, location = 'json')
            args = parser.parse_args()
            
            self.provider = args['provider']
            token = args['token']
            
            user = self.userCache[token]
            
            return user, 200
        except NameError:
            self.logger.warn("User authentication failed")
            restplus.abort(401)