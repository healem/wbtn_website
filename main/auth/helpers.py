#!../bin/python
import logging
from flask import session, flash, redirect, url_for
from validate_email import validate_email
from datastore import registerToBack, loginToBack
from session_cache import sessionCache
#from auth.routes import auth
#from utils import loginit

#loginit.initLogging()
logger = logging.getLogger(__name__)

def registerUser(token, email, provider=1):
    # Make sure email is populated
    if email is None:
        # flash no email, send back to register page
        flash("No email provided.  Please provide email address")
        return redirect(url_for("auth.register"))
    
    if validEmail(email) != True:
        # flash invalid email, send back to register page
        flash("Invalid email.  Please provide a valid email address")
        return redirect(url_for("auth.register"))
    
    logger.info("Registering user with token: {}".format(token))
    
    # call backend register
    backSess = registerToBack(token, email, provider)
    
    # Save session to cache
    sessionCache[token] = backSess
    
    # create session
    createSession(token)

def validEmail(email):
    return validate_email(email)
    
def loginUser(token, provider=1):
    logger.info("Logging in user with token: {}".format(token))
    # Call backend login
    backSess = loginToBack(token, provider)
    
    # Save session to cache
    sessionCache[token] = backSess
    
    # create session
    createSession(token)

def createSession(token):
    # Put it in the front session
    session['api_session_token'] = token
    
    ## Return session
    return 201
