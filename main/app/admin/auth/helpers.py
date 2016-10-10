#!/home/bythenum/public_html/whiskey/main/bin/python
import logging
from flask import session, flash, redirect, url_for, Response
from validate_email import validate_email
from app.admin.datastore import DataResponse, registerToBack, loginToBack
from app.admin.session_cache import sessionCache
from app.admin import admin

logger = logging.getLogger(__name__)

def registerUser(token, email, provider=1):
    if validEmail(email) != True:
        # flash invalid email, send back to register page
        flash("Invalid email.  Please provide a valid email address")
        return Response('INVALID_EMAIL', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})
    
    logger.info("Registering user with token: {}".format(token))
    
    # call backend register
    resp = registerToBack(token, email, provider)
    
    backSession = None
    if resp.status == 200:
        backSession = resp.data
    else:
        return resp.message
    
    # create session
    return createSession(token)

def validEmail(email):
    return validate_email(email)
    
def loginUser(token, provider=1):
    logger.info("Logging in user with token")
    # Call backend login
    resp = loginToBack(token, provider)
    
    user = None
    if resp.status == 200:
        user = resp.data
    else:
        return resp.message
    
    cacheUser(token, user)
    
    # create session
    return createSession(token)

def cacheUser(token, user):
    sessionCache[token] = user

def createSession(token):    
    # Put it in the front session
    session['api_session_token'] = token
    
    return 'OK'
