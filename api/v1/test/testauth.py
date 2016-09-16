#!../../bin/python
import unittest
import logging
from utils import loginit
import requests
from cookielib import CookieJar
import simplejson
import ConfigParser
    
class AuthTest(unittest.TestCase):
    
    configFile = "/home/bythenum/keys/wbtn.cnf"
    baseUrl = "https://whiskey.bythenums.com/api/v1/auth"

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        AuthTest.logger = logging.getLogger(__name__)
        AuthTest.config = ConfigParser.ConfigParser()
        AuthTest.config.read(AuthTest.configFile)
        AuthTest.userAccessToken = AuthTest.config.get("auth", "test_access_token")
        

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_registerUser(self):
        data = { 'token': AuthTest.userAccessToken, 'provider': 1, 'email': 'bqcrpft_romanstein_1473890065@tfbnw.net'}
        resp = requests.post("{}/register".format(AuthTest.baseUrl), data=data)
        AuthTest.logger.info("Register Response code: %s and response: %s ", resp.status_code, resp.content)
        AuthTest.logger.info("Register headers: %s and request headers: %s", resp.headers, resp.request.headers)
        
# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
    #logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
        
