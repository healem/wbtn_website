#!../../bin/python
import logging
from flask import session
from flask_restplus import Resource, Namespace, fields, reqparse
from cachetools import TTLCache

logger = logging.getLogger(self.logClassName)
api = Namespace('auth', description='User authentication and authorization related operations')

auth = api.model('Auth', {
    'token': fields.String(required=True, description='The user access token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
})

userCache = TTLCache(maxsize=500, ttl=3600, missing=getUser)
dbm = datastore.DbManager(testMode=False)

''' Wrapper: check required token '''
def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if 'api_session_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            logger.warn("User authentication failed, no token in session - please login")
            return restplus.abort(401, reason="NO_TOKEN")
        else:
            # validate token
            try:
                user = userCache[token]
            except (NameError):
                logger.warn("User authentication to social failed")
                return restplus.abort(401, reason="AUTH_FAILED")
            
            if user is None:
                # Validated by oauth to social, but no email, so we can't auto-register - need to register
                logger.info("User authenticated to social but does not have email - manual registration needed")
                return restplus.abort(401, reason="NO_EMAIL")

        # Auth successful - send them onward
        return func(*args, **kwargs)

    return check_token

# @api.route('/')
# class Auth(Resource):
#     
#     def __init__(self, err):
#         super(Users, self).__init__()
#         self.logClassName = '.'.join([__name__, self.__class__.__name__])
#         self.logger = logging.getLogger(self.logClassName)
#         self.provider = None      
#         
#     @api.expect(auth)
#     @api.param('provider', 'the provider of the token', 'formData')
#     @api.param('token', 'the access token from the provider', 'formData')
#     def post(self):
#         try:
#             parse = reqparse.RequestParser()
#             parse.add_argument('provider', type = str, location = 'json')
#             parse.add_argument('token', type = str, location = 'json')
#             args = parser.parse_args()
#             
#             self.provider = args['provider']
#             token = args['token']
#             
#             user = userCache[token]
#             
#             return user, 200
#         except NameError:
#             self.logger.warn("User authentication failed")
#             restplus.abort(401)

##################
## Helper functions
##################
def registerUser(token, provider, email):
    # Validate user is authenticated by social provider
    # Create local user account with provided email
    # Need to create secret key for signing the session with - store in config file
    # Create session
    # Return session
    
def loginUser(token, provider):
    auth = Social.get_provider(SocialType.provider)
    if auth is None:
        logger.warn("User authentication failed, no token in session - please login")
        return restplus.abort(401, reason="UNSUPPORTED_PROVIDER")
    
    user = getUser(token, provider)
    
    # Put it in the session
    session['api_session_token'] = token
    
    ## Return session
    
def getUser(token, provider=None):
    ## Verify the user is authenticated by social provider
    auth = Social.get_provider(SocialType.provider)
    if auth is None:
        # Force facebook, for now
        auth = 1
        logger.warn("User authentication failed, no token in session - please login")
        return restplus.abort(401, reason="UNSUPPORTED_PROVIDER")
    
    if auth.verify(token):
        ## Great!  Now lets see if they are registered with us
        ## First get email from social provider
        user = None
        userInfo = auth.getUserInfo(token)
        if 'email' in userInfo:
            user = dbm.getUserByEmail(email)
            if user is None:
                ## We don't have a local user - let's make one
                createLocalUser(userInfo)
                user = dbm.getUserByEmail(email)
        else:
            # facebook authentication successful, but no we don't have an email address
            # unable to create local account
            pass
        
        return user
    else:
        raise NameError("User failed authentication")

def createLocalUser(userInfo):
    socialId, firstName, lastName = None
    if 'id' in userInfo:
        socialId = userInfo['id']
    if 'first_name' in  userInfo:
        firstName = userInfo['first_name']
    if 'last_name' in userInfo:
        lastName = userInfo['last_name']
    dbm.addNormalUser(email=email, firstName=firstName, lastName=lastName, facebookId=socialId)