#!../../bin/python
import logging
from flask import session
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getUserFromSession(session):
    user = None
    # Check to see if it's in their session
    if 'api_session_token' not in session:
        logger.warn("User authentication failed, no token in session - please login")
    else:
        # validate token
        # Check if the session is in cache
        user = sessionCache.get(session['api_session_token'])
        if user is None:
            logger.debug("Session expired, reauthenticate with the backend")
        
    return user