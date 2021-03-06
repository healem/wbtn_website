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
        
#################################
##
##  Auth
##
#################################

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

#################################
##
##  User
##
#################################

def getMe(backSession):
    resp = backSession.get("{}/me".format(DATA_BASE_URL))
    #logger.debug("getMe raw response: {}".format(resp.json()))
    json = simplejson.loads(resp.json())
    
    #logger.debug("Get me response: {}".format(json))
    
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
    backSession = user.backSession
    #logger.debug("Backsession for getAllUsers: {}".format(backSession))
    data = { 'currentPage': currentPage, 'itemsPerPage': itemsPerPage }
    resp = backSession.get("{}/allusers".format(DATA_BASE_URL), data=data)
    
    #logger.debug("Response to getAllUsers: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return resp.json()

def updateUserInBack(email, permissionName, permissionValue):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'email': email, permissionName: permissionValue }
    resp = backSession.post("{}/user".format(DATA_BASE_URL), data=data)
    
    return handleResponse(resp)

def deleteUserInBack(email):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'email': email }
    resp = backSession.delete("{}/user".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to deleteUser: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

#################################
##
##  Whiskey
##
#################################

def getAllWhiskiesFromBack(currentPage, itemsPerPage, sortField=None, namesOnly=False):
    user = getUserFromSession(session)
    backSession = user.backSession
    #logger.debug("Backsession for getAllWhiskies: {}".format(backSession))
    data = { 'currentPage': currentPage, 'itemsPerPage': itemsPerPage, 'sortField': sortField, 'namesOnly': namesOnly }
    logger.info("Data for getAllWhiskiesFromBack {}".format(data))
    resp = backSession.get("{}/allwhiskies".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to getAllWhiskies: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return resp.json()

def addWhiskeyInBack(name, price, proof, style, age, url):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'name': name, 'price': price, 'proof': proof, 'style': style, 'age': age, 'url': url }
    resp = backSession.put("{}/whiskey".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to addWhiskey: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

def updateWhiskeyInBack(name, price, proof, style, age, icon, url):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'name': name, 'price': price, 'proof': proof, 'style': style, 'age': age, 'icon': icon, 'url': url }
    resp = backSession.post("{}/whiskey".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to updateWhiskey: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

def deleteWhiskeyInBack(name):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'name': name }
    resp = backSession.delete("{}/whiskey".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to deleteWhiskey: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

#################################
##
##  Rating
##
#################################

def getAllRatingsFromBack(currentPage, itemsPerPage, sortField=None):
    user = getUserFromSession(session)
    backSession = user.backSession
    #logger.debug("Backsession for getAllRatings: {}".format(backSession))
    data = { 'currentPage': currentPage, 'itemsPerPage': itemsPerPage, 'sortField': sortField }
    resp = backSession.get("{}/allratings".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to getAllRatings: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return resp.json()

def getRatingInBack(whiskeyId, userId):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'whiskeyId': whiskeyId, 'userId': userId }
    resp = backSession.get("{}/rating".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to getRating: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return resp.json()

def addRatingInBack(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'whiskeyId': whiskeyId, 'userId': userId, 'rating': rating, 'notes': notes, 'sweet': sweet, 'sour': sour, 'heat': heat, 'smooth': smooth, 'finish': finish, 'crisp': crisp, 'leather': leather, 'wood': wood, 'smoke': smoke, 'citrus': citrus, 'floral': floral, 'fruit': fruit}
    resp = backSession.put("{}/rating".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to addRating: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

def updateRatingInBack(whiskeyId, userId, rating, notes, sweet, sour, heat, smooth, finish, crisp, leather, wood, smoke, citrus, floral, fruit):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'whiskeyId': whiskeyId, 'userId': userId, 'rating': rating, 'notes': notes, 'sweet': sweet, 'sour': sour, 'heat': heat, 'smooth': smooth, 'finish': finish, 'crisp': crisp, 'leather': leather, 'wood': wood, 'smoke': smoke, 'citrus': citrus, 'floral': floral, 'fruit': fruit}
    resp = backSession.post("{}/rating".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to updateRating: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

def deleteRatingInBack(whiskeyId, userId):
    user = getUserFromSession(session)
    backSession = user.backSession
    data = { 'whiskeyId': whiskeyId, 'userId': userId }
    resp = backSession.delete("{}/rating".format(DATA_BASE_URL), data=data)
    
    logger.debug("Response to deleteRating: %s with data, headers: %s, original request url: %s", resp.content, resp.headers, resp.request.url)
    
    return handleResponse(resp)

#################################
##
##  Common
##
#################################
        
def handleResponse(resp, data=None):
    if resp.status_code == 200 or resp.status_code == 201:
        return DataResponse(status=200, data=data)
    elif resp.status_code == 401:
        return DataResponse(status=401, message=resp.json()["reason"])
    else:
        logger.error("Unhandled response: {}".format(resp.json()))
        flash("Contact support with error: {}".format(resp.json()))
        return DataResponse(status=500, message="Contact support with error: {}".format(resp.json()))


