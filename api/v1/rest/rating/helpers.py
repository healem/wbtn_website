#!../../../bin/python
import logging
import os.path
import urllib
import validators
from peewee import IntegrityError, DoesNotExist
from flask import session
from flask_restplus import abort
from db import datastore

logger = logging.getLogger(__name__)

dbm = datastore.DbManager(testMode=False)

def addRating(args):
    if "whiskeyId" not in args or args["whiskeyId"] is None:
        abort(400, reason="WHISKEY_ID_REQUIRED")
        
    if "userId" not in args or args["userId"] is None:
        abort(400, reason="USER_ID_REQUIRED")
        
    try:
        dbm.addUserRating(whiskeyId=args['whiskeyId'], userId=args['userId'], rating=args['rating'], notes=args['notes'], sweet=args['sweet'], sour=args['sour'], heat=args['heat'], smooth=args['smooth'], finish=args['finish'], crisp=args['crisp'], leather=args['leather'], wood=args['wood'], smoke=args['smoke'], citrus=args['citrus'], floral=args['floral'], fruit=args['fruit'])   
    except (IntegrityError):
        abort(400, reason="RATING_EXISTS")
        
    return 200

def deleteRating(args):
    if "whiskeyId" not in args or args["whiskeyId"] is None:
        abort(400, reason="WHISKEY_ID_REQUIRED")
        
    if "userId" not in args or args["userId"] is None:
        abort(400, reason="USER_ID_REQUIRED")
        
    try:
        dbm.deleteUserRatingByWhiskeyId(whiskeyId=args['whiskeyId'], userId=args['userId'])
    except (DoesNotExist):
        abort(400, reason="RATING_NOT_PRESENT")
        
    return 200

def updateRating(args):
    if "whiskeyId" not in args or args["whiskeyId"] is None:
        abort(400, reason="WHISKEY_ID_REQUIRED")
        
    if "userId" not in args or args["userId"] is None:
        abort(400, reason="USER_ID_REQUIRED")
        
    try:
        dbm.updateUserRating(whiskeyId=args['whiskeyId'], userId=args['userId'], rating=args['rating'], notes=args['notes'], sweet=args['sweet'], sour=args['sour'], heat=args['heat'], smooth=args['smooth'], finish=args['finish'], crisp=args['crisp'], leather=args['leather'], wood=args['wood'], smoke=args['smoke'], citrus=args['citrus'], floral=args['floral'], fruit=args['fruit'])   
    except (IntegrityError):
        abort(400, reason="UNKNOWN_ERROR")
        
    return 200
        
    