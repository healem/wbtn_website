#!../../../bin/python
import logging
from flask import session
from flask_restplus import abort
from db import datastore
from social.interface import Social
from social.factory import SocialFactory
from social.social_types import SocialType
from validate_email import validate_email
from rest.user_cache import userCache

logger = logging.getLogger(__name__)

dbm = datastore.DbManager(testMode=False)

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
    
    socialUser['email'] = email
    
    createLocalUser(socialUser)
    
    # Need to create secret key for signing the session with - store in config file
    # Create session
    return loginUser(token, provider)

def validEmail(email):
    return validate_email(email)
    
def loginUser(token, provider):
    # Validate user is authenticated by social provider
    socialUser = None
    try:
        socialUser = getSocialUser(token, provider)
    except (NameError):
        logger.warn("User authentication to social failed")
        return abort(401, reason="AUTH_FAILED")
    
    localUser = None
    if 'email' in socialUser:
        localUser = getLocalUser(socialUser['email'])
        if localUser is None:
            logger.warn("User auth to social succeeded, but local auth failed - %s might need to register?", socialUser['email'])
            return abort(401, reason="AUTH_FAILED")
    else:
        logger.error("Social user has no email, unable to complete login")
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
    logger.debug("Getting social user")
    socialUserInfo = getSocialUser(token, provider)
    if 'email' in socialUserInfo:
        logger.debug("Checking user with email %s", socialUserInfo['email'])
        localUser = getLocalUser(socialUserInfo['email'])
        if localUser is None:
            ## We don't have a local user - let's make one
            logger.debug("Creating local user for %s", socialUserInfo['email'])
            createLocalUser(userInfo)
            localUser = dbm.getUserByEmail(email)
    else:
        # facebook authentication successful, but no we don't have an email address
        # unable to create local account
        logger.warn("Unable to create local user for %s", socialUserInfo['email'])
        
    return localUser 
    
def getSocialUser(token, provider=None):
    ## Verify the user is authenticated by social provider
    logger.debug("Getting provider: %d", provider)
    try:
        auth = SocialFactory.get_provider(provider)
    except NameError as e:
        logger.error("Got exception: %s", e)
        
    if auth is None:
        logger.warn("User authentication failed, social provider not known. - please login using social media account")
        return abort(401, reason="UNSUPPORTED_PROVIDER")
    
    if auth.verify(token):
        logger.debug("User token verified")
        info = auth.getUserInfo(token)
        logger.debug("Got user info: %s", info)
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
    
def getUserFromSession(session):
    user = None
    # Check to see if it's in their session
    if 'api_session_token' not in session:
        # If it isn't return our access denied message (you can also return a redirect or render_template)
        logger.warn("User authentication failed, no token in session - please login")
        return abort(401, reason="NO_TOKEN")
    else:
        # validate token
        try:
            #user = userCache[session['api_session_token']]
            user = userCache.get(session['api_session_token'])
            if user is None:
                logger.debug("User not in cache - fetching from db")
                user = getUserWithAutoCreate(session['api_session_token'])
                # Got the user, now put it in cache
                userCache[session['api_session_token']] = user
                
            logger.debug("User cache entry: %s", user.__dict__)
                
        except (NameError):
            logger.warn("User authentication to social failed")
            return abort(401, reason="AUTH_FAILED")
        
        if user is None:
            # Validated by oauth to social, but no email, so we can't auto-register - need to register
            logger.debug("User authenticated to social but does not have email - manual registration needed")
            return abort(401, reason="NO_EMAIL")
        
    return user

def checkPermission(user, permission):
    if getattr(user,permission) == True:
        #logger.debug("%s granted access to %s", getattr(user, "email"), request.url)
        return True
    else:
        logger.warn("%s denied access to %s", getattr(user, "email"), request.url)
        return abort(401, reason="NO_PERMISSION")