#!/home/bythenum/public_html/whiskey/main/bin/python
import logging
import requests
import simplejson
from flask_restplus import abort
from .constants import DATA_BASE_URL

def register():
    backSess = requests.session(token, email, provider=1)
    data = { 'token': token, 'provider': provider, 'email': email}
    resp = backSess.post("{}/register".format(DATA_BASE_URL), data=data)
    
    if handleResponse(resp) is True:
        pass

def login():
    backSess = requests.session(token, provider=1)
    data = { 'token': token, 'provider': provider, 'email': email}
    resp = backSess.post("{}/register".format(DATA_BASE_URL), data=data)
    
    if handleResponse(resp) is True:
        pass
        
def handleResponse(resp):
    if resp.status_code == 200 or resp.status_code == 201:
        return True
    elif resp.status_code == 401:
        return handle_401(resp)
    else:
        # flash message below
        return abort(resp.status_code, reason="Contact support with error: {}".format(resp.json()["reason"]))
    
def handle_401(resp):
    if resp.json()["reason"] == "NO_EMAIL":
        #flash "No email address given" and return to registration form
        pass
    elif resp.json()["reason"]  == "INVALID_EMAIL":
        #flash "Invalid email address, please ensure your email address is entered correctly
        # return to registration form
        pass
    elif resp.json()["reason"]  == "AUTH_FAILED":
        #flash authentication to social media failed, return to social media login form
        pass
    elif resp.json()["reason"] == "UNSUPPORTED_PROVIDER":
        # flash please choose a supported social media to authenticate with, return to social media login form
        pass
    elif resp.json()["reason"] == "ALREADY_REGISTERED":
        # flash already registered, please login - return to login page
        pass
    elif resp.json()["reason"] == "ACCOUNT_NOT_UNIQUE":
        # flash user already taken, return to login page
        pass
    elif resp.json()["reason"] == "NO_PERMISSION":
        # flash no permission and return to front page
        pass
    else:
        # Unhandled error
        pass
