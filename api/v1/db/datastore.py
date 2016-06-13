#!../../bin/python

import models
import logging
import datetime
from peewee_wbtn import peewee_models
from peewee import IntegrityError
import ConfigParser

class DbManager():
    wbtnTables = [peewee_models.User, peewee_models.Whiskey, peewee_models.BlogEntry, peewee_models.CalculatedScores, peewee_models.UserRating]
    configFile = "/home4/healem/keys/wbtn.cnf"
    dbUser = "healem_wbtn"

    def __init__(self, testMode=False):
        self.logClassName = '.'.join([__name__, self.__class__.__name__])
        self.logger = logging.getLogger(self.logClassName)
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        self.testMode = testMode

        '''Get the password for config file'''
        self.logger.debug("Reading config file")
        self.dbPass = self.config.get("db", self.dbUser)

        '''Load test or prod db'''
        if self.testMode:
            self.logger.info("Loading test db")
            self.dbName = self.config.get("db", "test_db")
        else:
            self.logger.info("Loading production db")
            self.dbName = self.config.get("db", "prod_db")

        '''initialize the db'''
        self.logger.info("Initializing the database")
        self.db = peewee_models.BaseModel.getDbRef()
        self.db.init(self.dbName, user=self.dbUser, passwd=self.dbPass)

        '''make sure db tables are created'''
        self.logger.info("Creating tables, if needed")
        self.db.connect()
        self.db.create_tables(self.wbtnTables, safe=True)
        self.db.close

    # This method should only be used during testing
    '''Test accessor for raw db access'''
    def getDbInstance(self):
        return self.db

    #############################################
    ##
    ##
    ##  Methods on user table
    ##
    ##
    #############################################

    def addUser(self, email, userRater=False, blogWriter=False, collegeRater=False, whiskeyAdmin=False, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a new user to the database.  Must provide unique email address'''
        try:
            self.db.connect()
            with self.db.transaction():
                peewee_models.User.create(
                    firstName=firstName,
                    middleInitial=middleInitial,
                    lastName=lastName,
                    suffix=suffix,
                    email=email,
                    icon=icon,
                    createdTime=datetime.datetime.now(),
                    lastUpdatedTime=datetime.datetime.now(),
                    userRater=userRater,
                    blogWriter=blogWriter,
                    collegeRater=collegeRater,
                    whiskeyAdmin=whiskeyAdmin)
            self.db.close

        except IntegrityError:
            self.logger.error("Failed to add user %s, name already taken", email)
            self.db.close
            raise

    def addNormalUser(self, email, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a normal user that can give their rating of whiskeys'''
        self.addUser(email=email, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True)

    def addBlogWriterUser(self, email, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a user that can rate whiskeys and write blog entries'''
        self.addUser(email=email, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, blogWriter=True)

    def addCollegeRaterUser(self, email, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a user that can rate whiskeys and provide college ratings'''
        self.addUser(email=email, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, collegeRater=True)

    def addWhiskeyAdminUser(self, email, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a whiskey admin that can rate whiskeys, blog, and provide college ratings'''
        self.addUser(email=email, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, blogWriter=True, collegeRater=True, whiskeyAdmin=True)

    def getUserByEmail(self, email):
        '''Lookup a user by email address'''
        self.db.connect()
        user = peewee_models.User.get(peewee_models.User.email == email)
        wbtnUser = models.User(userId=user.id, email=user.email, firstName=user.firstName, middleInitial=user.middleInitial, lastName=user.lastName, suffix=user.suffix, icon=user.icon, userRater=user.userRater, blogWriter=user.blogWriter, collegeRater=user.collegeRater, whiskeyAdmin=user.whiskeyAdmin, createdTime=user.createdTime, lastUpdatedTime=user.lastUpdatedTime)
        self.db.close
        return wbtnUser

    def getUserById(self, userId):
        '''Lookup a user by userId'''
        self.db.connect()
        user = peewee_models.User.get(peewee_models.User.id == userId)
        wbtnUser = models.User(userId=user.id, email=user.email, firstName=user.firstName, middleInitial=user.middleInitial, lastName=user.lastName, suffix=user.suffix, icon=user.icon, userRater=user.userRater, blogWriter=user.blogWriter, collegeRater=user.collegeRater, whiskeyAdmin=user.whiskeyAdmin, createdTime=user.createdTime, lastUpdatedTime=user.lastUpdatedTime)
        self.db.close
        return wbtnUser

    def deleteUserByEmail(self, email):
        '''Delete a user by email address'''
        self.db.connect()
        self.logger.info("Deleteing user %s", email)
        query = peewee_models.User.delete().where(peewee_models.User.email == email)
        query.execute()
        self.db.close

    def deleteUserById(self, userId):
        '''Delete a user by userId'''
        self.db.connect()
        self.logger.info("Deleteing user %s", userId)
        query = peewee_models.User.delete().where(peewee_models.User.id == userId)
        query.execute()
        self.db.close

    def clearUserTable(self):
        self.db.connect()
        self.logger.info("Clearing user table")
        peewee_models.User.drop_table(True)
        self.db.create_tables([peewee_models.User], safe=True)
        self.db.close


if __name__ == "__main__":
    from utils import loginit
    loginit.initTestLogging()
    dbm = DbManager(testMode=True)
