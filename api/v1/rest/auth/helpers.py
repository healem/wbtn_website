#!../../bin/python
import logging
from flask import session, Blueprint
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from db import datastore
from social.interface import Social
from social.factory import SocialFactory
from social.social_types import SocialType
from validate_email import validate_email
#from utils import loginit

#loginit.initLogging()
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
    
    userInfo = { 'id': socialUser['id'],
                 'email': email }
    createLocalUser(userInfo)
    
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
    
    # Put it in the session
    session['api_session_token'] = token
    
    ## Return session
    return 201
    
def getUserWithAutoCreate(token, provider=None):
    ## Verify the user is authenticated by social provider
    logger.info("Entered getUserWithAutoCreate")
    if provider is None:
        provider = SocialType.facebook
    
    localUser = None
    logger.info("Getting social user")
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