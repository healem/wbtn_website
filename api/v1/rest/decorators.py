#!../../bin/python
import logging
from functools import wraps
from cachetools import TTLCache
from .auth import getUserWithAutoCreate

''' Wrapper: check required token '''
def require_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        getUserFromSession(session)

        # Auth successful - send them onward
        return func(*args, **kwargs)

    return check_token

''' Wrapper: check for admin permissions '''
def require_admin(func):
    @wraps(func)
    def check_admin(*args, **kwargs):
        user = getUserFromSession(session)
        checkPermission(user, 'whiskeyAdmin')
    
    return check_admin

''' Wrapper: check for blog permissions '''
def require_blog(func):
    @wraps(func)
    def check_blog(*args, **kwargs):
        user = getUserFromSession(session)
        checkPermission(user, 'blogWriter')
        
    return check_blog

''' Wrapper: check for college permissions '''
def require_college(func):
    @wraps(func)
    def check_college(*args, **kwargs):
        user = getUserFromSession(session)
        checkPermission(user, 'collegeRater')
    
    return check_college

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
            user = userCache[session['api_session_token']]
        except (NameError):
            logger.warn("User authentication to social failed")
            return abort(401, reason="AUTH_FAILED")
        
        if user is None:
            # Validated by oauth to social, but no email, so we can't auto-register - need to register
            logger.info("User authenticated to social but does not have email - manual registration needed")
            return abort(401, reason="NO_EMAIL")
        
    return user

def checkPermission(user, permission):
    if user[permission] == True:
        return True
    else:
        return abort(401, reason="NO_PERMISSION")
    
userCache = TTLCache(maxsize=500, ttl=3600, missing=getUserWithAutoCreate)