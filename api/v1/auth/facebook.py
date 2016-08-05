#!../../bin/python

import logging
from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service
import ConfigParser


class FacebookSignIn(object):
    configFile = "/home4/healem/keys/wbtn.cnf"
    facebookIdTag = "facebook_id"
    facebookSecretTag = "facebook_secret"

    def __init__(self):
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        
        '''Get get facebook app info from config file'''
        self.logger.debug("Reading config file")
        self.fbid = self.config.get("auth", self.facebookIdTag)
        self.fbsecret = self.config.get("auth", self.facebookSecretTag)
        
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.fbid,
            client_secret=self.fbsecret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def get_callback_url(self):
        return url_for('show_preloader_start_authentication', _external=True)

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='public_profile,email',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()})
        me = oauth_session.get('me?fields=id,email,first_name,last_name').json()
        return (
            me['id'],
            me.get('email'),
            me.get('first_name'),
            me.get('last_name')
)
