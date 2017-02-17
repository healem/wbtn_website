#!../../bin/python
import logging
from functools import wraps
from auth.helpers import getUserWithAutoCreate, checkPermission, getUserFromSession
from flask import session, request
from flask_restplus import abort

logger = logging.getLogger(__name__)

''' Wrapper: check required token '''
def require_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        logger.info("Checking for token")
        getUserFromSession(session)

        # Auth successful - send them onward
        return func(*args, **kwargs)

    return check_token

''' Wrapper: check for admin permissions '''
def require_admin(func):
    @wraps(func)
    def check_admin(*args, **kwargs):
        logger.info("Checking for user permissions")
        user = getUserFromSession(session)
        checkPermission(user, 'whiskeyAdmin')
        
        # Permissions successful - send them onward
        return func(*args, **kwargs)
    
    return check_admin

''' Wrapper: check for blog permissions '''
def require_blog(func):
    @wraps(func)
    def check_blog(*args, **kwargs):
        user = getUserFromSession(session)
        checkPermission(user, 'blogWriter')
        
        # Permissions successful - send them onward
        return func(*args, **kwargs)
        
    return check_blog

''' Wrapper: check for college permissions '''
def require_college(func):
    @wraps(func)
    def check_college(*args, **kwargs):
        user = getUserFromSession(session)
        checkPermission(user, 'collegeRater')
        
        # Permissions successful - send them onward
        return func(*args, **kwargs)
    
    return check_college

