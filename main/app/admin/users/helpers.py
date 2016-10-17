#!../bin/python
import logging
from app.admin import admin
from app.admin.datastore import DataResponse, getAllUsersFromBack
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getAllUsers(currentPage, itemsPerPage):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllUsersFromBack(currentPage, itemsPerPage)

