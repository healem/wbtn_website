#!../bin/python
import logging
from app.admin import admin
from app.admin.datastore import DataResponse, getAllWhiskiesFromBack, updateWhiskeyInBack, deleteWhiskeyInBack, addWhiskeyInBack, getAllRatingsFromBack, updateRatingInBack, deleteRatingInBack, addRatingInBack
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getAllWhiskies(currentPage, itemsPerPage, sortField):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllWhiskiesFromBack(currentPage, itemsPerPage, sortField)

def addWhiskey(name, price, proof, style, age, url):
    resp = addWhiskeyInBack(name, price, proof, style, age, url)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message

def updateWhiskey(name, price, proof, style, age, icon, url):
    resp = updateWhiskeyInBack(name, price, proof, style, age, icon, url)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message

def deleteWhiskey(name):
    resp = deleteWhiskeyInBack(name)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message
    
def getAllRatings(currentPage, itemsPerPage, sortField):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllRatingsFromBack(currentPage, itemsPerPage, sortField)

def addRating(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit):
    resp = addRatingInBack(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message

def updateRating(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit):
    resp = updateRatingInBack(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message

def deleteRating(whiskeyId, userId):
    resp = deleteRatingInBack(whiskeyId, userId)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message