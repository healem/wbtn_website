#!../../../bin/python
import logging
from peewee import DoesNotExist
from flask import session
from flask_restplus import abort
from db import datastore
from ..user_cache import userCache

logger = logging.getLogger(__name__)

dbm = datastore.DbManager(testMode=False)

def updateUser(args):
    if "email" not in args or args["email"] is None:
        abort(400, reason="EMAIL_REQUIRED")
    try:
        logger.debug("Args for updating user: %s", args)
        if args["firstname"] is not None:
            dbm.setFirstName(args["email"], args["firstName"])
        if args["lastname"] is not None:
            dbm.setLastName(args["email"], args["lastName"])
        if args["userId"] is not None:
            dbm.setSocialId(args["email"], args["userId"])
        if args["userRater"] is not None:
            dbm.setUserRater(args["email"], args["userRater"])
        if args["blogWriter"] is not None:
            dbm.setBlogWriter(args["email"], args["blogWriter"])
        if args["collegeRater"] is not None:
            dbm.setCollegeRater(args["email"], args["collegeRater"])
        if args["whiskeyAdmin"] is not None:
            dbm.setAdmin(args["email"], args["whiskeyAdmin"])
        if args["dumpCache"] is not None:
            cacheItems = userCache.items()
            for item in cacheItems:
                # cacheItem is a pair: (session_token, user)
                user = item[1]
                if user.email == args["email"]:
                    userCache.pop(item[0])
                    break
                
    except (DoesNotExist):
        abort(400, reason="BAD_EMAIL")
        
    return 200

def deleteUser(args):
    if "email" not in args or args["email"] is None:
        abort(400, reason="EMAIL_REQUIRED")
        
    try:
        dbm.deleteUserByEmail(args["email"])
    except (DoesNotExist):
        abort(400, reason="BAD_EMAIL")
        
    # Remove user from cache
    cacheItems = userCache.items()
    for item in cacheItems:
        # cacheItem is a pair: (session_token, user)
        user = item[1]
        if user.email == args["email"]:
            userCache.pop(item[0])
            break
        
    return 200