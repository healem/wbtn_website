#!/home/bythenum/public_html/whiskey/main/bin/python
import logging
import requests
import simplejson
from flask import redirect, url_for, flash
from constants import DATA_BASE_URL

def registerToBack(token, email, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider, 'email': email}
    resp = backSess.post("{}/register".format(DATA_BASE_URL), data=data)
    
    handleResponse(resp)
    
    return backSess

def loginToBack(token, provider):
    backSess = requests.session()
    data = { 'token': token, 'provider': provider }
    resp = backSess.post("{}/login".format(DATA_BASE_URL), data=data)
    
    handleResponse(resp)
    
    return backSess
        
def handleResponse(resp):
    if resp.status_code == 200 or resp.status_code == 201:
        return True
    elif resp.status_code == 401:
        return handle_401(resp)
    else:
        flash("Contact support with error: {}".format(resp.json()["reason"]))
        return redirect(url_for(login))
    
def handle_401(resp):
    if resp.json()["reason"] == "NO_EMAIL":
        flash("No email address - please provide email address")
        return redirect(url_for(register))
    elif resp.json()["reason"]  == "INVALID_EMAIL":
        flash("Invalid email address, please ensure your email address is entered correctly")
        return redirect(url_for(register))
    elif resp.json()["reason"]  == "AUTH_FAILED":
        flash("Login to social media failed")
        return redirect(url_for(login))
    elif resp.json()["reason"] == "UNSUPPORTED_PROVIDER":
        flash("Social media provider unsupported - please try a supported provider")
        return redirect(url_for(login))
    elif resp.json()["reason"] == "ALREADY_REGISTERED":
        flash("Already registered - please login")
        return redirect(url_for(login))
    elif resp.json()["reason"] == "ACCOUNT_NOT_UNIQUE":
        flash("This email address is already registered, please login or register with another email")
        return redirect(url_for(register))
    elif resp.json()["reason"] == "NO_PERMISSION":
        flash("You don't have permission to view this page")
        return redirect(url_for(login))
    else:
        # Unhandled error
        pass
