#!../../bin/python

import logging
from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service
from urllib2 import urlopen, HTTPError, HTTPCookieProcessor, build_opener, Request
from urllib import urlencode
from cookielib import CookieJar
from urlparse import parse_qsl
from functools import wraps
import simplejson
import ConfigParser
from users import TestUser
from social_types import SocialType
from interface import Social
import hashlib
import hmac

class FacebookError(HTTPError):
    def __init__(self, err):
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        try:
            data = simplejson.loads(err.fp.read().decode())['error']
            self.logger.debug("Raw error response: %s", data)
        except (ValueError, KeyError):
            # something REALLY bad happened and Facebook didn't send along
            # their usual error payload
            data = {
                'message': 'Unhandled error',
                'code': None,
                'type': None,
            }

        if '__debug__' in data:
            HTTPError.__init__(self, err.url, err.code, data['__debug__'],
                err.headers, err.fp)
        else:
            HTTPError.__init__(self, err.url, err.code, data['message'],
                err.headers, err.fp)

        self.api_code = data['code']
        self.type = data['type']
        
def translate_http_error(func):
    """ HTTPError to FacebookError translation decorator
    Decorates functions, handles :py:class:`urllib2.HTTPError` exceptions and
    translates them into :class:`FacebookError`
    :param func: The function to decorate with translation handling
    """
    @wraps(func)
    def inner(*args, **kwargs): # pylint: disable=C0111
        try:
            return func(*args, **kwargs)
        except HTTPError as err:
            raise FacebookError(err)
    return inner

class Facebook(Social):
    facebookIdTag = "facebook_id"
    facebookSecretTag = "facebook_secret"
    fbBaseUrl = "https://graph.facebook.com/v2.7/"

    def __init__(self):
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        
        '''Get get facebook app info from config file'''
        self.logger.debug("Reading config file")
        self.fbid = self.config.get("auth", self.facebookIdTag)
        self.fbsecret = self.config.get("auth", self.facebookSecretTag)
        
        super(Facebook, self).__init__(providerType=SocialType.facebook, appId=self.fbid, appSecret=self.fbsecret, baseUrl=self.fbBaseUrl)
        
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.appId,
            client_secret=self.appSecret,
            authorize_url='https://graph.facebook.com/v2.7/oauth/authorize',
            access_token_url='https://graph.facebook.com/v2.7/oauth/access_token',
            base_url=self.baseUrl
        )

    def authorize(self):
        self.logger.debug("Starting facebook authorization")
        return redirect(self.service.get_authorize_url(
            scope='public_profile,email',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))
    
    def callback(self):
        if 'code' not in request.args:
            self.logger.error("Failed to get facebook authorization: request arguments are wrong")
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()})
        me = oauth_session.get('me?fields=id,email,first_name,last_name').json()
        self.logger.debug("Facebook authorization succesful for email %s", me.get('email'))
        return (
            me['id'],
            me.get('email'),
            me.get('first_name'),
            me.get('last_name'))
    
    @translate_http_error
    def getUserInfo(self, accessToken):
        self.logger.debug("Getting user info")
        resp = urlopen('{}/me?{}'.format(self.baseUrl, urlencode({
            'fields': 'id,email,first_name,last_name',
            'access_token': accessToken,
            'appsecret_proof': self.genAppSecretProof(accessToken),
        })))
        
        r = simplejson.loads(resp.read().decode())
        self.logger.debug("Full response to get userInfo: %s", r)
        return r

    ''' Verify a user access token
        
        param accessToken: The user access token, returned by successful user login
        
        :return: True if token is good
    '''
    @translate_http_error
    def verify(self, accessToken):
        self.logger.info("Verifying facebook token")
        resp = urlopen('{}/debug_token?{}'.format(self.baseUrl, urlencode({
            'input_token': accessToken,
            'access_token': self.getAppAccessToken(),
        })))
        
        r = simplejson.loads(resp.read().decode())['data']
        if r['app_id'] == self.appId and r['is_valid']  == True:
            return True
        else:
            self.logger.error("Facebook token verify failed: expected %s and got %s: is_valid was %s", self.appId, r['app_id'], r['is_valid'])
            return False
            
    ''' Get an app access token from facebook - allows API access to app
        
        :return: app access token
    '''
    @translate_http_error
    def getAppAccessToken(self):
        resp = urlopen('{}oauth/access_token?{}'.format(self.baseUrl, urlencode({
            'client_id': self.appId,
            'client_secret': self.appSecret,
            'grant_type': 'client_credentials',
            'debug': 'all',
        })))
        
        r = simplejson.loads(resp.read().decode())['access_token']
        #self.logger.debug("Raw response: %s", r)
        
        return r
    
    ''' Get a list of facebook test users
    
        :param accessToken: The app access token, returned by getAppAccessToken
        
        :return: a list of user IDs
    '''
    @translate_http_error
    def getTestUsers(self, accessToken):
        resp = urlopen('{}/{}/accounts/test-users?{}'.format(self.baseUrl, self.appId, urlencode({
            'access_token': accessToken})))
        
        r = simplejson.loads(resp.read().decode())['data']
        
        ids = []
        for user in r:
            ids.append(user['id'])

        return ids
    
    ''' Get details for a single user
    
        :param accessToken: The app access token, returned by getAppAccessToken
        :param userId: The ID of the user to update, returned by getTestUsers or addTestUser
        
        :return a user object
    '''
    @translate_http_error
    def getTestUser(self, accessToken, userId):
        resp = urlopen('{}/{}?{}'.format(self.baseUrl, userId, urlencode({
            'method': 'get',
            'access_token': accessToken,
            'fields': 'id, name, email, locale'
        })))
    
        r = simplejson.loads(resp.read().decode())
        self.logger.debug("Full response to get user: %s", r)
        self.logger.debug("Got test user: %s", userId)
        
        e = None
        if 'email' in r:
            e = r['email']
        
        u = TestUser(userId=r['id'], email=e, userName=r['name'], password=None, locale=r['locale'], social=SocialType.facebook, loginUrl=None)
        
        return u
    
    ''' Creates a test user
    
        :param accessToken: The app access token, returned by getAppAccessToken
        :param userName: String with the userName - must meet facebook requirements of letters only
        :param locale(optional): String representing the locale for the user - default is "en_US"
        :param permissions(optional): Scope of the user.  A list of resources the test user has access to
                                       defaults to read_stream
        
        :return: a user object
    '''
    @translate_http_error
    def addTestUser(self, accessToken, userName, locale='en_US', permissions='read_stream, email'):
        resp = urlopen('{}/{}/accounts/test-users?{}'.format(self.baseUrl, self.appId, urlencode({
                'installed': True,
                'locale': locale,
                'permissions': permissions,
                'method': 'post',
                'access_token': accessToken,
                'name': userName,
        })))
        
        r = simplejson.loads(resp.read().decode())
        #self.logger.debug("Full response to add user: %s", r)
        self.logger.debug("Created user: %s with id: %s and locale: %s", r['email'], r['id'], locale)
        
        u = TestUser(userId=r['id'], email=r['email'], userName=userName, password=r['password'], locale=locale, social=SocialType.facebook, loginUrl=r['login_url'])

        return u
    
    ''' Deletes a test user
        
        :param accessToken: The app access token, returned by getAppAccessToken
        :param userId: The ID of the user to delete, returned by getTestUsers or addTestUser
        
        :return: true on success
    '''
    @translate_http_error
    def deleteTestUser(self, accessToken, userId):
        resp = urlopen('{}/{}?{}'.format(self.baseUrl, userId, urlencode({
            'method': 'delete',
            'access_token': accessToken,
        })))
        
        r = resp.read()
        self.logger.debug("Deleted user: %s with response: %s and code %d", userId, r, resp.code)

        if resp.code == 200:
            return True
        else:
            return False
    
    ''' Update username or password for a user ID
    
        :param accessToken: The app access token, returned by getAppAccessToken
        :param userId: The ID of the user to update, returned by getTestUsers or addTestUser
        :param userName(optional): New username for the given ID, only changed if new name given
        :param password(optional): New password for the given ID, only changed if new passowrd is given
        
        :return: true on success
    '''
    @translate_http_error
    def updateTestUser(self, accessToken, userId, userName=None, password=None):
        params = {
            'method': 'post',
            'access_token': accessToken,
        }
        
        if userName is not None:
            params['name'] = userName
            
        if password is not None:
            params['password'] = password
            
        resp = urlopen('{}/{}?{}'.format(self.baseUrl, userId, urlencode(params)))
        r = resp.read()
        
        self.logger.debug("Updated user id: %s with response %s and code %d", userId, r, resp.code)
        
        if resp.code == 200:
            return True
        else:
            return False
        
    ''' Generate appsecret_proof for facebook
    
        :param accessToken: the user access token for the account we are trying to access
        
        :return: the appsecret_proof
    '''
    def genAppSecretProof(self, accessToken):
        h = hmac.new (
            self.appSecret.encode('utf-8'),
            msg=accessToken.encode('utf-8'),
            digestmod=hashlib.sha256
        )
        return h.hexdigest()
     
''' This is meant for testing use only! '''   
class FacebookUser(object):
    jar = CookieJar()
    cookie = HTTPCookieProcessor(jar)       
    opener = build_opener(cookie)

    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "ISO-8859-1",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "m.facebook.com"
    }
    
    def __init__(self):
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
    
    @translate_http_error
    def login(self, email, password):
        params = {
            'email': email,
            'pass': password,
            'login':'Log+In',
            }
        
        req = Request('http://m.facebook.com/login.php?m=m&refsrc=m.facebook.com%2F', urlencode(params), self.headers)
        resp = self.opener.open(req)
        r = resp.read()

        self.logger.debug("Raw response from login request: %s with code %d", r, resp.code)
        
        if resp.code == 200:
            return True
        else:
            return False

    
