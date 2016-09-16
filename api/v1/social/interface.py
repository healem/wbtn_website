#!../../bin/python

import logging
from utils import loginit

class Social(object):
    providers = None
    providerType = None
    configFile = "/home/bythenum/keys/wbtn.cnf"
    appId = None
    appSecret = None
    baseUrl = None
    
    def __init__(self, providerType, appId, appSecret, baseUrl):
        self.providerType = providerType
        self.appId = appId
        self.appSecret = appSecret
        self.baseUrl = baseUrl

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.providerType, _external=True)

    def verify(self, accessToken):
        pass
