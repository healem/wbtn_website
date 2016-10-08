#!../bin/python
import logging
from flask import session, flash, redirect, url_for, Response
from validate_email import validate_email
from app.admin.datastore import DataResponse, registerToBack, loginToBack
from app.admin.session_cache import sessionCache
from app.admin import admin

#loginit.initLogging()
logger = logging.getLogger(__name__)

def registerUser(token, email, provider=1):
    if validEmail(email) != True:
        # flash invalid email, send back to register page
        flash("Invalid email.  Please provide a valid email address")
        return Response('INVALID_EMAIL', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})
    
    logger.info("Registering user with token: {}".format(token))
    
    # call backend register
    resp = registerToBack(token, email, provider)
    
    # create session
    return createSession(token, resp)

def validEmail(email):
    return validate_email(email)
    
def loginUser(token, provider=1):
    logger.info("Logging in user with token: {}".format(token))
    # Call backend login
    resp = loginToBack(token, provider)
    
    # create session
    return createSession(token, resp)

def createSession(token, dataResponse):
    # Check if we successfully got the session
    if dataResponse.status == 200:
        # Save the session to cache
        sessionCache[token] = dataResponse.backSession
        
        # Put it in the front session
        session['api_session_token'] = token
        
        return 'OK'
    else:
        return dataResponse.message
