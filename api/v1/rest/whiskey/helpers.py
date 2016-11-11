#!../../../bin/python
import logging
from peewee import IntegrityError, DoesNotExist
from flask import session
from flask_restplus import abort
from db import datastore

logger = logging.getLogger(__name__)

dbm = datastore.DbManager(testMode=False)

def addWhiskey(args):
    if "name" not in args or args["name"] is None:
        abort(400, reason="NAME_REQUIRED")
        
    try:
        dbm.addWhiskey(name=args['name'], price=args['price'], proof=args['proof'], style=args['style'], age=args['age'], icon=args['icon'], url=args['url'])   
    except (IntegrityError):
        abort(400, reason="NAME_TAKEN")
        
    return 200

def deleteWhiskey(args):
    if "name" not in args or args["name"] is None:
        abort(400, reason="NAME_REQUIRED")
        
    try:
        dbm.deleteWhiskeyByName(args["name"])
    except (DoesNotExist):
        abort(400, reason="BAD_NAME")
        
    return 200

def updateWhiskey(args):
    if "name" not in args or args["name"] is None:
        abort(400, reason="NAME_REQUIRED")
    try:
        logger.debug("Args for updating whiskey: %s", args)
        if args["name"] is not None:
            dbm.setName(args["name"], args["name"])
        if args["price"] is not None:
            dbm.setPrice(args["name"], args["price"])
        if args["proof"] is not None:
            dbm.setProof(args["name"], args["proof"])
        if args["style"] is not None:
            dbm.setStyle(args["name"], args["style"])
        if args["age"] is not None:
            dbm.setAge(args["name"], args["age"])
        if args["icon"] is not None:
            dbm.setIcon(args["name"], args["icon"])
        if args["url"] is not None:
            dbm.setUrl(args["name"], args["url"])         
    except (DoesNotExist):
        abort(400, reason="BAD_EMAIL")
    except (IntegrityError):
        abort(400, reason="NAME_TAKEN")
        
    return 200