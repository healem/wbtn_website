#!../bin/python
import logging
from app.admin import admin
from app.admin.datastore import DataResponse, getAllWhiskiesFromBack, updateWhiskeyInBack, deleteWhiskeyInBack, addWhiskeyInBack
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getAllWhiskies(currentPage, itemsPerPage, sortField):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllWhiskiesFromBack(currentPage, itemsPerPage, sortField)

def addWhiskey(name):
    return 'OK'

def updateWhiskey(name):
    return 'OK'

def deleteWhiskey(name):
    resp = deleteWhiskeyInBack(name)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message