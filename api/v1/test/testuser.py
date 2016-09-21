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
    email2 = 'yssxozk_ricewitz_1474412890@tfbnw.net'
    dbm = None

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        UserTest.logger = logging.getLogger(__name__)
        UserTest.config = ConfigParser.ConfigParser()
        UserTest.config.read(UserTest.configFile)
        UserTest.userAccessToken = UserTest.config.get("auth", "test_access_token")
        UserTest.userAccessToken2 = UserTest.config.get("auth", "test_access_token2")
        
        # DB setup
        UserTest.dbm = datastore.DbManager(testMode=False)

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_getUser(self):
        # Clear out users from previous tests
        if self.dbm.getUserByEmail(UserTest.email) is not None:
            self.dbm.deleteUserByEmail(UserTest.email)
        if self.dbm.getUserByEmail(UserTest.email2) is not None:
            self.dbm.deleteUserByEmail(UserTest.email2)
            
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
        
        # Try to get my info
        resp4 = sess.get("{}/me".format(UserTest.baseUrl))
        UserTest.logger.debug("Get me Response code: %s and response: %s ", resp4.status_code, resp4.content)
        UserTest.logger.debug("Get me headers: %s and request headers: %s", resp4.headers, resp4.request.headers)
        self.assertEqual(resp4.status_code, 200)
        
        # Register second test user
        sess2 = requests.session()
        data4 = { 'token': UserTest.userAccessToken2, 'provider': UserTest.provider, 'email': UserTest.email2}
        resp5 = sess2.post("{}/register".format(UserTest.baseUrl), data=data4)
        self.assertEqual(resp2.status_code, 200)
        
        # Get user successfully
        # directly set admin in db and dump server cache of session
        self.dbm.setAdmin(UserTest.email, True)
        resp6 = sess.put("{}/me".format(UserTest.baseUrl))
        UserTest.logger.debug("Get user Response code: %s and response: %s ", resp6.status_code, resp6.content)
        UserTest.logger.debug("Get user headers: %s and request headers: %s", resp6.headers, resp6.request.headers)
        self.assertEqual(resp6.status_code, 200)
        
        # Now successfully get user
        data5 = {'email': UserTest.email}
        resp7 = sess.get("{}/user".format(UserTest.baseUrl), data=data5)
        UserTest.logger.debug("Get user Response code: %s and response: %s ", resp7.status_code, resp7.content)
        UserTest.logger.debug("Get user headers: %s and request headers: %s", resp7.headers, resp7.request.headers)
        self.assertEqual(resp7.status_code, 200)
        
        # Now update second user
        data6 = {'email': UserTest.email2, 'blogWriter': True, 'dumpCache': True}
        resp8 = sess.post("{}/user".format(UserTest.baseUrl), data=data6)
        UserTest.logger.debug("Update user Response code: %s and response: %s ", resp8.status_code, resp8.content)
        UserTest.logger.debug("Update user headers: %s and request headers: %s", resp8.headers, resp8.request.headers)
        self.assertEqual(resp8.status_code, 200)
        
        # Clean up test users
        self.dbm.deleteUserByEmail(UserTest.email)
        self.dbm.deleteUserByEmail(UserTest.email2)
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()