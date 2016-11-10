#!../bin/python
import logging
from app.admin import admin
from app.admin.datastore import DataResponse, getAllUsersFromBack, updateUserInBack, deleteUserInBack
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getAllWhiskies(currentPage, itemsPerPage, sortField):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllWhiskiesFromBack(currentPage, itemsPerPage, sortField)