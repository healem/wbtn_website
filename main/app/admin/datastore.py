#!/home/bythenum/public_html/whiskey/main/bin/python
import logging
import requests
import simplejson
from flask import redirect, url_for, flash
from app.constants import DATA_BASE_URL
from app.admin import admin

logger = logging.getLogger(__name__)

class DataResponse(object):
    def __init__(self, status, backSession=None, message=None):
        self.status = status
        self.backSession = backSession
        self.message = message

def registerToBack(token, email, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider, 'email': email}
    resp = backSess.post("{}/register".format(DATA_BASE_URL), data=data)
    
    logger.debug("Register to back response: {}".format(resp.json()))
    
    return handleResponse(resp, backSess)

def loginToBack(token, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider }
    resp = backSess.post("{}/login".format(DATA_BASE_URL), data=data)
    
    logger.debug("Login to back response: {}".format(resp.json()))
    
    return handleResponse(resp, backSess)
        
def handleResponse(resp, backSession):
    if resp.status_code == 200 or resp.status_code == 201:
        return DataResponse(200, backSession)
    elif resp.status_code == 401:
        return DataResponse(401, None, resp.json()["reason"])
        #return handle_401(resp)
    else:
        logger.error("Unhandled response: {}".format(resp.json()))
        flash("Contact support with error: {}".format(resp.json()))
        return DataResponse(500, None, "Contact support with error: {}".format(resp.json()))
        #return redirect(url_for(admin.login))
    
def handle_401(resp):
    if resp.json()["reason"] == "NO_EMAIL":
        flash("No email address - please provide email address")
        return redirect(url_for(admin.register))
    elif resp.json()["reason"]  == "INVALID_EMAIL":
        flash("Invalid email address, please ensure your email address is entered correctly")
        return redirect(url_for(admin.register))
    elif resp.json()["reason"]  == "AUTH_FAILED":
        flash("Login to social media failed")
        return redirect(url_for(admin.login))
    elif resp.json()["reason"] == "UNSUPPORTED_PROVIDER":
        flash("Social media provider unsupported - please try a supported provider")
        return redirect(url_for(admin.login))
    elif resp.json()["reason"] == "ALREADY_REGISTERED":
        flash("Already registered - please login")
        return redirect(url_for(admin.login))
    elif resp.json()["reason"] == "ACCOUNT_NOT_UNIQUE":
        flash("This email address is already registered, please login or register with another email")
        return redirect(url_for(admin.register))
    elif resp.json()["reason"] == "NO_PERMISSION":
        flash("You don't have permission to view this page")
        return redirect(url_for(admin.login))
    else:
        # Unhandled error
        pass
