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

    #############################################
    ##
    ##
    ##  Methods for user table
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
        
    #############################################
    ##
    ##
    ##  Methods for Whiskey table
    ##
    ##
    #############################################

    def addWhiskey(self, name, price=None, proof=None, style=None, age=None, icon=None):
        '''Add a new whiskey to the database.  Must provide unique name'''
        try:
            self.db.connect()
            with self.db.transaction():
                peewee_models.Whiskey.create(
                    name=name,
                    price=price,
                    proof=proof,
                    style=style,
                    age=age,
                    icon=icon,
                    createdTime=datetime.datetime.now(),
                    lastUpdatedTime=datetime.datetime.now())
            self.db.close

        except IntegrityError:
            self.logger.error("Failed to add whiskey %s, name already taken", name)
            self.db.close
            raise
        
    def getWhiskeyByName(self, name):
        '''Lookup a whiskey by name'''
        self.db.connect()
        whiskey = peewee_models.Whiskey.get(peewee_models.Whiskey.name == name)
        wbtnWhiskey = models.Whiskey(whiskeyId=whiskey.id, name=whiskey.name, price=whiskey.price, proof=whiskey.proof, style=whiskey.style, age=whiskey.age, icon=whiskey.icon, createdTime=whiskey.createdTime, lastUpdatedTime=whiskey.lastUpdatedTime)
        self.db.close
        return wbtnWhiskey

    def getWhiskeyById(self, whiskeyId):
        '''Lookup whiskey by ID'''
        self.db.connect()
        whiskey = peewee_models.Whiskey.get(peewee_models.Whiskey.id == whiskeyId)
        wbtnWhiskey = models.Whiskey(whiskeyId=whiskey.id, name=whiskey.name, price=whiskey.price, proof=whiskey.proof, style=whiskey.style, age=whiskey.age, icon=whiskey.icon, createdTime=whiskey.createdTime, lastUpdatedTime=whiskey.lastUpdatedTime)
        self.db.close
        return wbtnWhiskey

    def deleteWhiskeyByName(self, name):
        '''Delete a whiskey by name'''
        self.db.connect()
        self.logger.info("Deleteing whiskey %s", name)
        query = peewee_models.Whiskey.delete().where(peewee_models.Whiskey.name == name)
        query.execute()
        self.db.close

    def deleteWhiskeyById(self, whiskeyId):
        '''Delete a whiskey by whiskeyId'''
        self.db.connect()
        self.logger.info("Deleteing whiskey %s", whiskeyId)
        query = peewee_models.Whiskey.delete().where(peewee_models.Whiskey.id == whiskeyId)
        query.execute()
        self.db.close

    def clearWhiskeyTable(self):
        self.db.connect()
        self.logger.info("Clearing whiskey table")
        peewee_models.Whiskey.drop_table(True)
        self.db.create_tables([peewee_models.Whiskey], safe=True)
        self.db.close
        
    #############################################
    ##
    ##
    ##  Methods for BlogEntry table
    ##
    ##
    #############################################

    def addBlogEntry(self, userId, title, text):
        '''Add a new blog entry to the database.  Must provide unique title'''
        try:
            self.db.connect()
            with self.db.transaction():
                peewee_models.BlogEntry.create(
                    userId=userId,
                    title=title,
                    text=text,
                    createdTime=datetime.datetime.now(),
                    lastUpdatedTime=datetime.datetime.now())
            self.db.close

        except IntegrityError:
            self.logger.error("Failed to add blog entry %s, title already taken", title)
            self.db.close
            raise
        
    def getBlogEntryByTitle(self, title):
        '''Lookup a blog entry by title'''
        self.db.connect()
        blog = peewee_models.BlogEntry.get(peewee_models.BlogEntry.title == title)
        wbtnBlog = models.BlogEntry(blogEntryId=blog.id, title=blog.title, userId=blog.id, text=blog.text, createdTime=blog.createdTime, lastUpdatedTime=blog.lastUpdatedTime)
        self.db.close
        return wbtnBlog

    def getBlogEntryById(self, blogEntryId):
        '''Lookup a blog entry by ID'''
        self.db.connect()
        blog = peewee_models.BlogEntry.get(peewee_models.BlogEntry.id == blogEntryId)
        wbtnBlog = models.BlogEntry(blogEntryId=blog.id, title=blog.title, userId=blog.id, text=blog.text, createdTime=blog.createdTime, lastUpdatedTime=blog.lastUpdatedTime)
        self.db.close
        return wbtnBlog

    def deleteBlogEntryByTitle(self, title):
        '''Delete a blog entry by title'''
        self.db.connect()
        self.logger.info("Deleteing blog entry %s", title)
        query = peewee_models.BlogEntry.delete().where(peewee_models.BlogEntry.title == title)
        query.execute()
        self.db.close

    def deleteBlogEntryById(self, blogEntryId):
        '''Delete a blog entry by blogEntryId'''
        self.db.connect()
        self.logger.info("Deleteing blog entry %s", blogEntryId)
        query = peewee_models.BlogEntry.delete().where(peewee_models.BlogEntry.id == blogEntryId)
        query.execute()
        self.db.close

    def clearBlogEntryTable(self):
        self.db.connect()
        self.logger.info("Clearing blog entry table")
        peewee_models.BlogEntry.drop_table(True)
        self.db.create_tables([peewee_models.BlogEntry], safe=True)
        self.db.close

