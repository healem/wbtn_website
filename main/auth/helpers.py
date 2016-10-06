#!../bin/python
import logging
from flask import session, flash, redirect, url_for
from validate_email import validate_email
from datastore import registerToBack, loginToBack
from session_cache import sessionCache
#from utils import loginit

#loginit.initLogging()
logger = logging.getLogger(__name__)

def registerUser(token, email, provider=1):
    # Make sure email is populated
    if email is None:
        # flash no email, send back to register page
        flash("No email provided.  Please provide email address")
        return redirect(url_for(register))
    
    if validEmail(email) != True:
        # flash invalid email, send back to register page
        flash("Invalid email.  Please provide a valid email address")
        return redirect(url_for(register))
    
    # call backend register
    backSess = registerToBack(token, provider, email)
    
    # Save session to cache
    sessionCache[token] = backSess
    
    # create session
    createSession(token)

def validEmail(email):
    return validate_email(email)
    
def loginUser(token, provider=1):
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
