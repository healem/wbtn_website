#!../../bin/python
import unittest
import logging
from utils import loginit
from db import datastore
import requests
import simplejson
import ConfigParser

class WhiskeyTest(unittest.TestCase):
    
    configFile = "/home/bythenum/keys/wbtn.cnf"
    baseUrl = "https://whiskey.bythenums.com/api/v1"
    provider = 1
    email = 'bqcrpft_romanstein_1473890065@tfbnw.net'
    email2 = 'yssxozk_ricewitz_1474412890@tfbnw.net'
    dbm = None
    
    wname1 = "Test Whiskey 1"
    wproof1 = 40
    wprice1 = 35.00
    wage1 = 10
    wstyle1 = "Style1"

    wname2 = "Test Whiskey 2"
    wproof2 = 80
    wprice2 = 70.00
    wage2 = 20
    wstyle2 = "Style2"

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        WhiskeyTest.logger = logging.getLogger(__name__)
        WhiskeyTest.config = ConfigParser.ConfigParser()
        WhiskeyTest.config.read(WhiskeyTest.configFile)
        WhiskeyTest.userAccessToken = WhiskeyTest.config.get("auth", "test_access_token")
        WhiskeyTest.userAccessToken2 = WhiskeyTest.config.get("auth", "test_access_token2")
        
        # DB setup
        WhiskeyTest.dbm = datastore.DbManager(testMode=False)

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_getWhiskey(self):
        # Clear out users from previous tests
        if self.dbm.getUserByEmail(WhiskeyTest.email) is not None:
            self.dbm.deleteUserByEmail(WhiskeyTest.email)
        if self.dbm.getUserByEmail(WhiskeyTest.email2) is not None:
            self.dbm.deleteUserByEmail(WhiskeyTest.email2)
            
        # Register test user
        sess = requests.session()
        data = { 'token': WhiskeyTest.userAccessToken, 'provider': WhiskeyTest.provider, 'email': WhiskeyTest.email}
        resp = sess.post("{}/register".format(WhiskeyTest.baseUrl), data=data)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp.status_code, resp.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp.headers, resp.request.headers)
        self.assertEqual(resp.status_code, 200)
        
        # Give test user admin directly in database
        # Flush session cache on the server so we get updated permissions
        self.dbm.setAdmin(WhiskeyTest.email, True)
        resp = sess.put("{}/me".format(WhiskeyTest.baseUrl))
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp.status_code, resp.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp.headers, resp.request.headers)
        self.assertEqual(resp.status_code, 200)
        
        # Register second test user (not admin)
        sess1 = requests.session()
        data1 = { 'token': WhiskeyTest.userAccessToken2, 'provider': WhiskeyTest.provider, 'email': WhiskeyTest.email2}
        resp1 = sess1.post("{}/register".format(WhiskeyTest.baseUrl), data=data1)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp1.status_code, resp1.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp1.headers, resp1.request.headers)
        self.assertEqual(resp1.status_code, 200)
        
        # Add test whiskey
        data2 = { 'name': WhiskeyTest.wname1, 'proof': WhiskeyTest.wproof1, 'price': WhiskeyTest.wprice1, 'age': WhiskeyTest.wage1, 'style': WhiskeyTest.wstyle1 }
        resp2 = sess.put("{}/whiskey".format(WhiskeyTest.baseUrl), data=data2)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp2.status_code, resp2.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp2.headers, resp2.request.headers)
        self.assertEqual(resp2.status_code, 200)
        
        # Try to get whiskey with session but no admin permissions
        data3 = {'name': WhiskeyTest.wname1}
        resp3 = sess1.get("{}/whiskey".format(WhiskeyTest.baseUrl), data=data3)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp3.status_code, resp3.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp3.headers, resp3.request.headers)
        self.assertEqual(resp3.status_code, 200)
        
        # Try to update whiskey without admin permissions
        data4 = {'name': WhiskeyTest.wname1, 'price': WhiskeyTest.wprice2}
        resp4 = sess1.post("{}/whiskey".format(WhiskeyTest.baseUrl), data=data4)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp4.status_code, resp4.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp4.headers, resp4.request.headers)
        self.assertEqual(resp4.status_code, 401)
        self.assertEqual(resp4.json()['reason'], 'NO_PERMISSION')
        
        # Try to add whiskey without admin
        data5 = { 'name': WhiskeyTest.wname2, 'proof': WhiskeyTest.wproof2, 'price': WhiskeyTest.wprice2, 'age': WhiskeyTest.wage2, 'style': WhiskeyTest.wstyle2 }
        resp5 = sess1.put("{}/whiskey".format(WhiskeyTest.baseUrl), data=data5)
        self.assertEqual(resp5.status_code, 401)
        self.assertEqual(resp5.json()['reason'], 'NO_PERMISSION')
        
        # Try to delete whiskey without admin
        data6 = {'name': WhiskeyTest.wname1}
        resp6 = sess1.delete("{}/whiskey".format(WhiskeyTest.baseUrl), data=data6)
        self.assertEqual(resp6.status_code, 401)
        self.assertEqual(resp6.json()['reason'], 'NO_PERMISSION')
        
        # Update whiskey with admin permissions
        data7 = {'name': WhiskeyTest.wname1, 'price': WhiskeyTest.wprice2}
        resp7 = sess.post("{}/whiskey".format(WhiskeyTest.baseUrl), data=data7)
        WhiskeyTest.logger.debug("Get user Response code: %s and response: %s ", resp7.status_code, resp7.content)
        WhiskeyTest.logger.debug("Get user headers: %s and request headers: %s", resp7.headers, resp7.request.headers)
        self.assertEqual(resp7.status_code, 200)
        
        # Delete whiskey with admin
        data8 = {'name': WhiskeyTest.wname1}
        resp8 = sess.delete("{}/whiskey".format(WhiskeyTest.baseUrl), data=data8)
        self.assertEqual(resp8.status_code, 200)
        
        # Clean up test whiskies
        if self.dbm.getWhiskeyByName(WhiskeyTest.wname1) is not None:
            self.dbm.deleteWhiskeyByName(WhiskeyTest.wname1)
        if self.dbm.getWhiskeyByName(WhiskeyTest.wname2) is not None:
            self.dbm.deleteWhiskeyByName(WhiskeyTest.wname2)
        
        # Clean up test users
        if self.dbm.getUserByEmail(WhiskeyTest.email) is not None:
            self.dbm.deleteUserByEmail(WhiskeyTest.email)
        if self.dbm.getUserByEmail(WhiskeyTest.email2) is not None:
            self.dbm.deleteUserByEmail(WhiskeyTest.email2)
            
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
        
        