#!../../bin/python
import unittest
import logging
from utils import loginit
from db import datastore
import requests
import simplejson
import ConfigParser

class UserTest(unittest.TestCase):
    
    configFile = "/home/bythenum/keys/wbtn.cnf"
    baseUrl = "https://whiskey.bythenums.com/api/v1"
    provider = 1
    email = 'bqcrpft_romanstein_1473890065@tfbnw.net'
    dbm = None

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        UserTest.logger = logging.getLogger(__name__)
        UserTest.config = ConfigParser.ConfigParser()
        UserTest.config.read(UserTest.configFile)
        UserTest.userAccessToken = UserTest.config.get("auth", "test_access_token")
        
        # DB setup
        UserTest.dbm = datastore.DbManager(testMode=False)

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_getUser(self):
        # Clear out user from previous tests
        if self.dbm.getUserByEmail(UserTest.email) is not None:
            self.dbm.deleteUserByEmail(UserTest.email)
            
        # Try to get user without session
        data = {'email': UserTest.email}
        resp = requests.get("{}/user".format(UserTest.baseUrl), data=data)
        UserTest.logger.debug("Get user Response code: %s and response: %s ", resp.status_code, resp.content)
        UserTest.logger.debug("Get user headers: %s and request headers: %s", resp.headers, resp.request.headers)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json()['reason'], 'NO_TOKEN')
        
        # Register test user
        sess = requests.session()
        data2 = { 'token': UserTest.userAccessToken, 'provider': UserTest.provider, 'email': UserTest.email}
        resp2 = sess.post("{}/register".format(UserTest.baseUrl), data=data2)
        self.assertEqual(resp2.status_code, 200)
        
        # Try to get user with session but no admin permissions
        data3 = {'email': UserTest.email}
        resp3 = sess.get("{}/user".format(UserTest.baseUrl), data=data3)
        UserTest.logger.debug("Get user Response code: %s and response: %s ", resp3.status_code, resp3.content)
        UserTest.logger.debug("Get user headers: %s and request headers: %s", resp3.headers, resp3.request.headers)
        self.assertEqual(resp3.status_code, 401)
        self.assertEqual(resp3.json()['reason'], 'NO_PERMISSION')
        
        # Get user successfully
        self.dbm.setAdmin(UserTest.email, True)
        data4 = {'email': UserTest.email}
        resp4 = sess.get("{}/user".format(UserTest.baseUrl), data=data4)
        UserTest.logger.debug("Get user Response code: %s and response: %s ", resp4.status_code, resp4.content)
        UserTest.logger.debug("Get user headers: %s and request headers: %s", resp4.headers, resp4.request.headers)
        self.assertEqual(resp2.status_code, 200)
        
        # Clean up test user
        self.dbm.deleteUserByEmail(UserTest.email)
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()