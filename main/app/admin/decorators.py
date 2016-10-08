#!../../bin/python
import logging
from functools import wraps
from flask import session, redirect, url_for
from app.admin.session_cache import sessionCache
from app.admin import admin

logger = logging.getLogger(__name__)

''' Wrapper: check required token '''
def require_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        getBackSession(session)

        # Auth successful - send them onward
        return func(*args, **kwargs)

    return check_token

''' Wrapper: check for admin permissions '''
def require_admin(func):
    @wraps(func)
    def check_admin(*args, **kwargs):
        bs = getBackSession(session)
        
        # don't blindly trust the session, verify locally if user has rights
        checkPermission(bs, 'whiskeyAdmin')
    
    return check_admin

''' Wrapper: check for blog permissions '''
def require_blog(func):
    @wraps(func)
    def check_blog(*args, **kwargs):
        bs = getBackSession(session)
        
        # don't blindly trust the session, verify locally if user has rights
        checkPermission(bs, 'blogWriter')
        
    return check_blog

''' Wrapper: check for college permissions '''
def require_college(func):
    @wraps(func)
    def check_college(*args, **kwargs):
        bs = getBackSession(session)
        
        # don't blindly trust the session, verify locally if user has rights
        checkPermission(bs, 'collegeRater')
    
    return check_college

def getBackSession(session):
    user = None
    # Check to see if it's in their session
    if 'api_session_token' not in session:
        logger.warn("User authentication failed, no token in session - please login")
        #return redirect(url_for("admin.login"))
        return redirect("https://whiskey.bythenums.com/main/login")
    else:
        # validate token
        # Check if the session is in cache
        sess = sessionCache.get(session['api_session_token'])
        if sess is None:
            logger.debug("Session expired, reauthenticate with the backend")
            #return redirect(url_for(admin.login))
            return redirect("https://whiskey.bythenums.com/main/login")
        
    return sess

def checkPermission(backSession, permission):
    logger.info("Backsession: %s", backSession)
    if backSession[permission] == True:
        return True
    else:
        return abort(401, reason="NO_PERMISSION")