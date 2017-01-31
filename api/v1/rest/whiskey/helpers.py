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

def addWhiskey(args):
    if "name" not in args or args["name"] is None:
        abort(400, reason="NAME_REQUIRED")
        
    icon = downloadImage(args['url'])
        
    try:
        dbm.addWhiskey(name=args['name'], price=args['price'], proof=args['proof'], style=args['style'], age=args['age'], icon=icon, url=args['url'])   
    except (IntegrityError):
        abort(400, reason="NAME_TAKEN")
        
    return 200

def deleteWhiskey(args):
    if "name" not in args or args["name"] is None:
        abort(400, reason="NAME_REQUIRED")
        
    try:
        deleteIcon(dbm.getWhiskeyByName(args["name"]).icon)
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
        if args["url"] is not None:
            if args['icon'] is None:
                args["icon"] = downloadImage(args['url'])
            dbm.setUrl(args["name"], args["url"])
        if args["icon"] is not None:
            ## First, delete the old icon, if it exists
            deleteIcon(dbm.getWhiskeyByName(args["name"]).icon)
            dbm.setIcon(args["name"], args["icon"])
    except (DoesNotExist):
        abort(400, reason="BAD_EMAIL")
    except (IntegrityError):
        abort(400, reason="NAME_TAKEN")
        
    return 200

def downloadImage(url):
    imageDir = "/home/bythenum/public_html/whiskey/api/v1/static/img/"
    filename = url.split('/')[-1]
    extension = os.path.splitext(filename)[1]
    
    if not validators.url(url):
        logger.error("Invalid url: {}".format(url))
        abort(400, reason="INVALID_URL")
    
    if extension not in ['.png', '.jpg', '.jpeg']:
        logger.error("Unsupport image format: {}".format(extension))
        abort(400, reason="UNSUPPORT_IMG_FORMAT")
    
    if os.path.isfile(filename):
        logger.warn("File exists, overwriting {}".format(filename))
        
    urllib.urlretrieve(url, "{}{}".format(imageDir, filename))
    
    return "https://whiskey.bythenums.com/api/v1/static/img/{}".format(filename)

def deleteIcon(icon):
    imageDir = "/home/bythenum/public_html/whiskey/api/v1/static/img/"
    filename = icon.split('/')[-1]
    fullname = "{}{}".format(imageDir, filename)
    
    try:
        logger.debug("Deleting file: {}".format(fullname))
        os.remove(fullname)
    except OSError:
        # Fail silently - as long as the file is gone, we don't really care
        pass
        
    