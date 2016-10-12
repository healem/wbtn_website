#!/home/bythenum/public_html/whiskey/main/bin/python
import logging
import requests
import simplejson
from flask import redirect, url_for, flash, session
from app.constants import DATA_BASE_URL
from app.admin import admin
from app.admin.user import User
from app.admin.utils import getUserFromSession

logger = logging.getLogger(__name__)

class DataResponse(object):
    def __init__(self, status, message=None, data=None):
        self.status = status
        self.message = message
        self.data = data

def registerToBack(token, email, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider, 'email': email}
    resp = backSess.post("{}/register".format(DATA_BASE_URL), data=data)
    
    logger.debug("Register to back response: {}".format(resp.json()))
    
    return handleResponse(resp, data=backSess)

def loginToBack(token, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider }
    resp = backSess.post("{}/login".format(DATA_BASE_URL), data=data)
    
    logger.debug("Login to back response: {}".format(resp.json()))
    
    # Check if login was successful before continuing
    user = None
    validResp = handleResponse(resp)
    if validResp.status == 200:
        user = getMe(backSess)
    else:
        return validResp
    
    return handleResponse(resp, data=user)

def getMe(backSession):
    resp = backSession.get("{}/me".format(DATA_BASE_URL))
    logger.debug("getMe raw response: {}".format(resp.json()))
    json = simplejson.loads(resp.json())
    
    logger.debug("Get me response: {}".format(json))
    
    user = User(userId=json["userId"],
                email=json['email'],
                createdTime=json['createdTime'],
                backSession=backSession,
                userRater=json['userRater'],
                blogWriter=json['blogWriter'],
                collegeRater=json['collegeRater'],
                whiskeyAdmin=json['whiskeyAdmin'],
                socialId=json['socialId'],
                firstName=json['firstName'],
                middleInitial=json['middleInitial'],
                lastName=json['lastName'],
                suffix=json['suffix'],
                lastUpdatedTime=json['lastUpdatedTime'],
                icon=json['icon'])
    
    return user

def getAllUsersFromBack(currentPage, itemsPerPage):
    user = getUserFromSession(session)
    backSession = user['backSession']
    data = { 'currentPage': currentPage, 'itemsPerPage': itemsPerPage }
    resp = backSession.get("{}/users".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to getAllUsers: {}".format(resp.json()))
    
    return resp.json()
        
def handleResponse(resp, data=None):
    if resp.status_code == 200 or resp.status_code == 201:
        return DataResponse(status=200, data=data)
    elif resp.status_code == 401:
        return DataResponse(status=401, message=resp.json()["reason"])
    else:
        logger.error("Unhandled response: {}".format(resp.json()))
        flash("Contact support with error: {}".format(resp.json()))
        return DataResponse(status=500, message="Contact support with error: {}".format(resp.json()))


