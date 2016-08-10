#!../../bin/python

import sys
import logging
import unittest
import ConfigParser
from utils import loginit
from social import facebook
from social import users
from social.social_types import Social

class FBTest(unittest.TestCase):
    configFile = "/home4/healem/keys/wbtn.cnf"
    fb = None
    accessToken = None
    userAccessToken = None

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        FBTest.fb = facebook.Facebook()
        FBTest.accessToken = FBTest.fb.getAppAccessToken()
        
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        FBTest.userAccessToken = self.config.get("auth", "test_access_token")
        
    @classmethod
    def tearDownClass(cls):
        users = FBTest.fb.getTestUsers(accessToken=FBTest.accessToken)
        for user in users:
            tmpUser = FBTest.fb.getTestUser(accessToken=FBTest.accessToken, userId=user)
            if tmpUser.userName != "Open Graph Test User":
                FBTest.fb.deleteTestUser(accessToken=FBTest.accessToken, userId=user)
        
    def test_addTestUser(self):
        u1 = 'ATestUseraskhjfdgal'
        loc1 = 'en_US'
        tu = FBTest.fb.addTestUser(accessToken=FBTest.accessToken, userName=u1)
        self.assertEqual(tu.userName, u1)
        self.assertIsNotNone(tu.password)
        self.assertEqual(tu.locale, loc1)
        self.assertIsNotNone(tu.email)
        self.assertIsNotNone(tu.userId)
        self.assertEqual(tu.social, Social.facebook)
        
        u2 = 'BTestUseraskhjfdgal'
        loc2 = 'es_ES'
        tu2 = FBTest.fb.addTestUser(accessToken=FBTest.accessToken, userName=u2, locale=loc2)
        self.assertEqual(tu2.userName, u2)
        self.assertIsNotNone(tu2.password)
        self.assertEqual(tu2.locale, loc2)
        self.assertIsNotNone(tu2.email)
        self.assertIsNotNone(tu2.userId)
        self.assertEqual(tu2.social, Social.facebook)
        
    def test_updateTestUser(self):
        u3 = 'CTestUseraskhjfdgal'
        u4 = 'DTestUseraskhjfdgal'
        loc1 = 'en_US'
        tu3 = FBTest.fb.addTestUser(accessToken=FBTest.accessToken, userName=u3)
        self.assertTrue(FBTest.fb.updateTestUser(accessToken=FBTest.accessToken, userId=tu3.userId, userName=u4, password='sdhaerhsdg'))
        tu4 = FBTest.fb.getTestUser(accessToken=FBTest.accessToken, userId=tu3.userId)
        self.assertEqual(tu4.userName, u4)
       
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()


