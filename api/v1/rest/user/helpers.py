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
        if "firstName" in args:
            dbm.setFirstName(args["email"], args["firstName"])
        if "lastName" in args:
            dbm.setLastName(args["email"], args["lastName"])
        if "userId" in args:
            dbm.setSocialId(args["email"], args["userId"])
        if "userRater" in args:
            dbm.setUserRater(args["email"], args["userRater"])
        if "blogWriter" in args:
            dbm.setBlogWriter(args["email"], args["blogWriter"])
        if "collegeRater" in args:
            dbm.setCollegeRater(args["email"], args["collegeRater"])
        if "whiskeyAdmin" in args:
            dbm.setAdmin(args["email"], args["whiskeyAdmin"])
        if "dumpCache" in  args:
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