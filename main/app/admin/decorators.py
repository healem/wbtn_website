#!../../bin/python
import logging
from functools import wraps
from flask import session, redirect, url_for, flash
from app.admin.session_cache import sessionCache
from app.admin import admin
from app.admin.utils import getUserFromSession

logger = logging.getLogger(__name__)

''' Wrapper: check required token '''
def require_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if getUserFromSession(session) is None:
            flash("No active session - please login")
            return redirect("https://whiskey.bythenums.com/main/login")
        else:
            # Auth successful - send them onward
            return func(*args, **kwargs)

    return check_token

''' Wrapper: check for admin permissions '''
def require_admin(func):
    @wraps(func)
    def check_admin(*args, **kwargs):
        # don't blindly trust the session, verify locally if user has rights
        if checkPermission('whiskeyAdmin') == True:
            # Permission check successful - send them onward
            return func(*args, **kwargs)
        else:
            flash("Admin permissions required.  Please login as a valid admin.")
            return redirect("https://whiskey.bythenums.com/main/denied")
    
    return check_admin

''' Wrapper: check for blog permissions '''
def require_blog(func):
    @wraps(func)
    def check_blog(*args, **kwargs):
        # don't blindly trust the session, verify locally if user has rights
        if checkPermission('blogWriter') == True:
            # Permission check successful - send them onward
            return func(*args, **kwargs)
        else:
            flash("Blog writer permissions required.  Please login with a valid blog writer account.")
            return redirect("https://whiskey.bythenums.com/main/denied")
        
    return check_blog

''' Wrapper: check for college permissions '''
def require_college(func):
    @wraps(func)
    def check_college(*args, **kwargs):
        # don't blindly trust the session, verify locally if user has rights
        if checkPermission('collegeRater') == True:
            # Permission check successful - send them onward
            return func(*args, **kwargs)
        else:
            flash("College rating permissions required.  Please login with a valid college rater account.")
            return redirect("https://whiskey.bythenums.com/main/denied")
    
    return check_college

def checkPermission(permission):
    user = getUserFromSession(session)
    
    if user is None:
        return False
    
    if getattr(user, permission) == True:
        return True
    else:
        return False