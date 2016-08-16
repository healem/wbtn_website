#!../../bin/python

import logging

class Social(object):
    providers = None
    providerType = None
    configFile = "/home4/healem/keys/wbtn.cnf"
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

    @classmethod
    def get_provider(self, providerType):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.providerType] = provider
        return self.providers[providerType]
    
    def verify(self, accessToken):
        pass