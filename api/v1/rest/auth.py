#!../../bin/python
import logging
from flask import session, Blueprint
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from restplus import api
from db import datastore
from social.interface import Social
from social.factory import SocialFactory
from validate_email import validate_email

logger = logging.getLogger(__name__)
authApi = Namespace('auth', description='User authentication and authorization related operations')

authRegister = authApi.model('Register', {
    'token': fields.String(required=True, description='The user access token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
    'email': fields.String(required=True, description='Email address of the user'),
})

authLogin = authApi.model('Login', {
    'token': fields.String(required=True, description='The user access token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
})

regParser = aauthApi.parser()
regParser.add_argument('token', type=str, required=True, help='The user access token')
regParser.add_argument('provider', type=int, required=True, help='The provider the token belongs to')
regParser.add_argument('email', type=str, required=True, help='Email address of the user')

loginParser = authApi.parser()
loginParser.add_argument('token', type=str, required=True, help='The user access token')
loginParser.add_argument('provider', type=int, required=True, help='The provider the token belongs to')

dbm = datastore.DbManager(testMode=False)

@api.route('/register')
@api.expect(regParser)
class AuthRegister(Resource):
    @api.marshal_list_with(authRegister)
    def post(self):
        args = regParser.parse_args()
        return registerUser(args['token'], args['provider'], args['email'])

def registerUser(token, provider, email):
    # Make sure email is populated
    if email is None:
        return abort(401, reason="NO_EMAIL")
    
    if validEmail(email) != True:
        return abort(401, reason="INVALID_EMAIL")
    
    # Validate user is authenticated by social provider
    socialUser = None
    try:
        socialUser = getSocialUser(token, provider)
    except (NameError):
        logger.warn("User authentication to social failed")
        return abort(401, reason="AUTH_FAILED")
    
    # Verify there is no email associated with this social id
    # Protection from DOS based on valid facebook user registering many emails (creating many users)
    result = socialIdNotAssociatedWithEmail(socialUser['id'])
    if result != True:
        return abort(401, reason=result)
    
    # Create local user account with provided email
    if socialUser is None:
        logger.warn("User authentication to social failed")
        return abort(401, reason="AUTH_FAILED")
    
    userInfo = { 'id': socialUser['id'],
                 'email': email }
    createLocalUser(userInfo)
    
    # Need to create secret key for signing the session with - store in config file
    # Create session
    return loginUser(token, provider)

def validEmail(email):
    return validate_email(email)
    
@api.route('/login')
@api.expect(loginParser)
class AuthLogin(Resource):
    @api.marshal_list_with(authLogin)
    def post(self):
        args = loginParser.parse_args()
        return loginUser(args['token'], args['provider'])
    
def loginUser(token, provider):
    # Validate user is authenticated by social provider
    socialUser = None
    try:
        socialUser = getSocialUser(token, provider)
    except (NameError):
        logger.warn("User authentication to social failed")
        return abort(401, reason="AUTH_FAILED")
    
    # Put it in the session
    session['api_session_token'] = token
    
    ## Return session
    return 201
    
def getUserWithAutoCreate(token, provider=None):
    ## Verify the user is authenticated by social provider
    if provider is None:
        provider = SocialType.facebook
    
    localUser = None
    socialUserInfo = getSocialUser(token, provider)
    if 'email' in socialUserInfo:
        localUser = getLocalUser(socialUserInfo['email'])
        if localUser is None:
            ## We don't have a local user - let's make one
            createLocalUser(userInfo)
            localUser = dbm.getUserByEmail(email)
    else:
        # facebook authentication successful, but no we don't have an email address
        # unable to create local account
        pass
        
    return localUser 
    
def getSocialUser(token, provider=None):
    ## Verify the user is authenticated by social provider
    logger.info("Getting provider: %d", provider)
    try:
        auth = SocialFactory.get_provider(provider)
    except NameError as e:
        logger.error("Got exception: %s", e)
        
    logger.info("Got auth: %s ", auth)
    if auth is None:
        logger.warn("User authentication failed, social provider not known. - please login using social media account")
        return abort(401, reason="UNSUPPORTED_PROVIDER")
    
    if auth.verify(token):
        logger.info("User token verified")
        info = auth.getUserInfo(token)
        logger.info("Got user info: %s", info)
        return info
    else:
        logger.error("User token failed verification")
        raise NameError("User failed authentication")
    
def socialIdNotAssociatedWithEmail(socialId):
    users = []
    users = dbm.getUsersBySocialId(socialId)
    numUsers = len(users)
    if numUsers ==  0:
        return True
    elif numUsers == 1:
        return "ALREADY_REGISTERED"
    else:
        return "ACCOUNT_NOT_UNIQUE"
    
def getLocalUser(email):
    user = None
    user = dbm.getUserByEmail(email)
    return user

def createLocalUser(userInfo):
    socialId = None
    firstName = None
    lastName = None
    if 'id' in userInfo:
        socialId = userInfo['id']
    if 'first_name' in  userInfo:
        firstName = userInfo['first_name']
    if 'last_name' in userInfo:
        lastName = userInfo['last_name']
    dbm.addNormalUser(email=userInfo['email'], firstName=firstName, lastName=lastName, socialId=socialId)