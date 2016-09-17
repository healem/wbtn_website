#!../../bin/python
import unittest
import logging
from utils import loginit
from db import datastore
import requests
from cookielib import CookieJar
import simplejson
import ConfigParser
    
class AuthTest(unittest.TestCase):
    
    configFile = "/home/bythenum/keys/wbtn.cnf"
    baseUrl = "https://whiskey.bythenums.com/api/v1/auth"
    provider = 1
    email = 'bqcrpft_romanstein_1473890065@tfbnw.net'
    dbm = None

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        AuthTest.logger = logging.getLogger(__name__)
        AuthTest.config = ConfigParser.ConfigParser()
        AuthTest.config.read(AuthTest.configFile)
        AuthTest.userAccessToken = AuthTest.config.get("auth", "test_access_token")
        
        # DB setup
        AuthTest.dbm = datastore.DbManager(testMode=False)

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_registerUser(self):
        # Clear out user from previous tests
        if self.dbm.getUserByEmail(AuthTest.email) is not None:
            self.dbm.deleteUserByEmail(AuthTest.email)
            
        data = { 'token': AuthTest.userAccessToken, 'provider': AuthTest.provider, 'email': AuthTest.email}
        resp = requests.post("{}/register".format(AuthTest.baseUrl), data=data)
        AuthTest.logger.debug("Register Response code: %s and response: %s ", resp.status_code, resp.content)
        AuthTest.logger.debug("Register headers: %s and request headers: %s", resp.headers, resp.request.headers)
        self.assertEqual(resp.status_code, 200)
        
        # Now register again - should fail
        resp2 = requests.post("{}/register".format(AuthTest.baseUrl), data=data)
        AuthTest.logger.debug("Register Response code: %s and response: %s ", resp2.status_code, resp2.content)
        AuthTest.logger.debug("Register headers: %s and request headers: %s", resp2.headers, resp2.request.headers)
        self.assertEqual(resp2.status_code, 401)
        self.assertEqual(resp2.json()['reason'], 'ALREADY_REGISTERED')
        
        # Test login
        data2 = { 'token': AuthTest.userAccessToken, 'provider': AuthTest.provider}
        resp3 = requests.post("{}/login".format(AuthTest.baseUrl), data=data2)
        AuthTest.logger.debug("Register Response code: %s and response: %s ", resp3.status_code, resp3.content)
        AuthTest.logger.debug("Register headers: %s and request headers: %s", resp3.headers, resp3.request.headers)
        self.assertEqual(resp.status_code, 200)
        
        # Now register with no email
        data3 = { 'token': AuthTest.userAccessToken, 'provider': AuthTest.provider, 'email': None}
        resp4 = requests.post("{}/register".format(AuthTest.baseUrl), data=data3)
        AuthTest.logger.debug("Register Response code: %s and response: %s ", resp4.status_code, resp4.content)
        self.assertEqual(resp4.status_code, 400)
        
        # Register with invalid email
        data4 = { 'token': AuthTest.userAccessToken, 'provider': AuthTest.provider, 'email': "sdfhrt"}
        resp5 = requests.post("{}/register".format(AuthTest.baseUrl), data=data4)
        AuthTest.logger.debug("Register Response code: %s and response: %s ", resp5.status_code, resp5.content)
        self.assertEqual(resp5.status_code, 401)
        self.assertEqual(resp5.json()['reason'], 'INVALID_EMAIL')
        
        # Clean up test user
        self.dbm.deleteUserByEmail(AuthTest.email)
        
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
        
