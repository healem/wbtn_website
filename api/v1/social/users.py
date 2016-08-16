#!../../bin/python

class User(object):
    def __init__(self, userId, email=None, userName=None, locale=None, social=None, loginUrl=None):
        self.userId = userId
        self.email = email
        self.userName = userName
        self.locale = locale
        self.social = social
        self.loginUrl = loginUrl
        
class TestUser(User):
    def __init__(self, userId, email=None, userName=None, password=None, locale=None, social=None, loginUrl=None):
        super(TestUser, self).__init__(userId, email, userName, locale, social, loginUrl)
        self.password = password