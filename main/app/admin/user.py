#!../../bin/python

class User(object):

    def __init__(self, userId, email, createdTime, backSession, userRater=True, blogWriter=False, collegeRater=False, whiskeyAdmin=False, socialId=None, firstName=None, middleInitial=None, lastName=None, suffix=None, lastUpdatedTime=None, icon=None):
        self.userId = userId
        self.firstName = firstName
        self.middleInitial = middleInitial
        self.lastName = lastName
        self.suffix = suffix
        self.email = email
        self.socialId = socialId
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime
        self.icon = icon
        self.userRater = userRater
        self.blogWriter = blogWriter
        self.collegeRater = collegeRater
        self.whiskeyAdmin = whiskeyAdmin
        self.backSession = backSession