#!../bin/python
import logging
from app.admin import admin
from app.admin.datastore import DataResponse, getAllUsersFromBack, updateUserInBack, deleteUserInBack
from app.admin.session_cache import sessionCache

logger = logging.getLogger(__name__)

def getAllUsers(currentPage, itemsPerPage):
    #logger.debug("In helper: getting %d page with %d items per page", currentPage, itemsPerPage)
    return getAllUsersFromBack(currentPage, itemsPerPage)

def updateUser(email, permissionName, permissionValue):
    # translate javascript true/false into python True/False
    if permissionValue == "true":
        permissionValue = True
    elif permissionValue == "false":
        permissionValue = False
    else:
        return "ERROR: invalid permission value of {}".format(permissionValue)
    
    resp = updateUserInBack(email, permissionName, permissionValue)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message
    
def deleteUser(email):
    resp = deleteUserInBack(email)
    
    if resp.status == 200:
        return 'OK'
    else:
        return resp.message


