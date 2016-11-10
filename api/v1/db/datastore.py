#!../../bin/python

import models
import logging
import datetime
import simplejson
from peewee_wbtn import peewee_models
from peewee import IntegrityError, DoesNotExist
from playhouse.shortcuts import model_to_dict
import ConfigParser

class DbManager(object):
    wbtnTables = [peewee_models.User, peewee_models.Whiskey, peewee_models.BlogEntry, peewee_models.CalculatedScore, peewee_models.UserRating]
    configFile = "/home/bythenum/keys/wbtn.cnf"
    dbUser = "bythenum_wbtn"

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
        else: # pragma: no cover
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

    def addUser(self, email, socialId=None, userRater=False, blogWriter=False, collegeRater=False, whiskeyAdmin=False, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
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
                    socialId=socialId,
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

    def addNormalUser(self, email, socialId=None, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a normal user that can give their rating of whiskeys'''
        self.addUser(email=email, socialId=socialId, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True)

    def addBlogWriterUser(self, email, socialId=None, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a user that can rate whiskeys and write blog entries'''
        self.addUser(email=email, socialId=socialId, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, blogWriter=True)

    def addCollegeRaterUser(self, email, socialId=None, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a user that can rate whiskeys and provide college ratings'''
        self.addUser(email=email, socialId=socialId, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, collegeRater=True)

    def addWhiskeyAdminUser(self, email, socialId=None, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None):
        '''Add a whiskey admin that can rate whiskeys, blog, and provide college ratings'''
        self.addUser(email=email, socialId=socialId, firstName=firstName, middleInitial=middleInitial, lastName=lastName, suffix=suffix, icon=icon, userRater=True, blogWriter=True, collegeRater=True, whiskeyAdmin=True)

    def addFacebookAccountToUser(self, userId, socialId):
        '''Add a facebook account to an existing user'''
        lastUpdatedTime = datetime.datetime.now()
        query = peewee_models.User.update(lastUpdatedTime=lastUpdatedTime, socialId=socialId).where(peewee_models.User.id == userId)
        rowsUpdated = 0
        self.db.connect()
        with self.db.transaction():
            rowsUpdated = query.execute()
        self.db.close
        
        if rowsUpdated == 0:
            self.logger.error("Unable to add facebook account: User %s not found", userId)
            raise DoesNotExist("Did not find user %s", userId)
        elif rowsUpdated > 1:
            self.logger.error("%d users found for id %s", rowsUpdated, userId)
            raise IntegrityError("%d rows found with userId %s", rowsUpdated, userId)
        
    def getAllUsers(self, currentPage, itemsPerPage):
        ''' Get all users - paged.  First page returned is 1 (not 0)'''
        self.logger.debug("Requesting page %d from allUsers", currentPage)
        # Cap itemsPerPage at 100
        if itemsPerPage > 100:
            self.logger.warn("Requested %d itemsPerPage exceeded max of 100", itemsPerPage)
            itemsPerPage = 100
        users = []
        self.db.connect()
        for user in peewee_models.User.select(peewee_models.User.firstName,
                                              peewee_models.User.lastName,
                                              peewee_models.User.email,
                                              peewee_models.User.userRater,
                                              peewee_models.User.blogWriter,
                                              peewee_models.User.collegeRater,
                                              peewee_models.User.whiskeyAdmin).order_by(peewee_models.User.lastName).paginate(currentPage, itemsPerPage):
            users.append(model_to_dict(user))
        self.db.close
        
        self.logger.debug("Returning users: %s", simplejson.dumps(users))
        
        return simplejson.dumps(users)
        
    def setUserRater(self, email, isUserRater):
        ''' Give the user normal rating permissions '''
        self.logger.info("Setting user %s rating permissions to %s", email, isUserRater)
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(userRater=isUserRater,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setAdmin(self, email, isAdmin):
        ''' Give the user admin permissions '''
        self.logger.info("Setting user %s admin permissions to %s", email, isAdmin)
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(whiskeyAdmin=isAdmin,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setBlogWriter(self, email, isBlogWriter):
        ''' Give the user blog writing permissions '''
        self.logger.info("Setting user %s blogWriter permissions to %s", email, isBlogWriter)
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(blogWriter=isBlogWriter,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setCollegeRater(self, email, isCollegeRater):
        ''' Give the user college rating permissions '''
        self.logger.info("Setting user %s collegeRater permissions to %s", email, isCollegeRater)
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(collegeRater=isCollegeRater,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setFirstName(self, email, firstName):
        '''Update the user's firstname'''
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(firstName=firstName,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setLastName(self, email, lastName):
        '''Update the user's lastname'''
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(lastName=lastName,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close
        
    def setEmail(self, currentEmail, newEmail):
        '''Update the user's email'''
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(email=newEmail,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == currentEmail)
            query.execute()
        self.db.close
        
    def setSocialId(self, email, socialId):
        '''Update the user's social ID'''
        self.db.connect()
        with self.db.transaction():
            query = peewee_models.User.update(socialId=socialId,lastUpdatedTime=datetime.datetime.now()).where(peewee_models.User.email == email)
            query.execute()
        self.db.close

    def getUserByEmail(self, email):
        '''Lookup a user by email address'''
        wbtnUser = None
        self.db.connect()
        try:
            user = peewee_models.User.get(peewee_models.User.email == email)
            wbtnUser = models.User(userId=user.id, email=user.email, socialId=user.socialId, firstName=user.firstName, middleInitial=user.middleInitial, lastName=user.lastName, suffix=user.suffix, icon=user.icon, userRater=user.userRater, blogWriter=user.blogWriter, collegeRater=user.collegeRater, whiskeyAdmin=user.whiskeyAdmin, createdTime=user.createdTime, lastUpdatedTime=user.lastUpdatedTime)
        except DoesNotExist:
            pass
            
        self.db.close
        return wbtnUser

    def getUserById(self, userId):
        '''Lookup a user by userId'''
        wbtnUser = None
        self.db.connect()
        try:
            user = peewee_models.User.get(peewee_models.User.id == userId)
            wbtnUser = models.User(userId=user.id, email=user.email, socialId=user.socialId, firstName=user.firstName, middleInitial=user.middleInitial, lastName=user.lastName, suffix=user.suffix, icon=user.icon, userRater=user.userRater, blogWriter=user.blogWriter, collegeRater=user.collegeRater, whiskeyAdmin=user.whiskeyAdmin, createdTime=user.createdTime, lastUpdatedTime=user.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnUser
    
    def getUsersBySocialId(self, socialId):
        ''' Lookup a user by social id - this could return more than one entry '''
        wbtnUsers = []
        self.db.connect()
        try:
            users = peewee_models.User.select().where(peewee_models.User.socialId == socialId)
            for user in users:
                wbtnUser = models.User(userId=user.id, email=user.email, socialId=user.socialId, firstName=user.firstName, middleInitial=user.middleInitial, lastName=user.lastName, suffix=user.suffix, icon=user.icon, userRater=user.userRater, blogWriter=user.blogWriter, collegeRater=user.collegeRater, whiskeyAdmin=user.whiskeyAdmin, createdTime=user.createdTime, lastUpdatedTime=user.lastUpdatedTime)
                wbtnUsers.append(wbtnUser)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnUsers

    def deleteUserByEmail(self, email):
        '''Delete a user by email address'''
        self.db.connect()
        self.logger.info("Deleting user %s", email)
        
        try:
            with self.db.transaction():
                query = peewee_models.User.delete().where(peewee_models.User.email == email)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete user %s", email)
            self.db.close
            raise
        
        self.db.close

    def deleteUserById(self, userId):
        '''Delete a user by userId'''
        self.db.connect()
        self.logger.info("Deleting user %s", userId)
        try:
            with self.db.transaction():
                query = peewee_models.User.delete().where(peewee_models.User.id == userId)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete user %d", userId)
            self.db.close
            raise
        
        self.db.close

    def clearUserTable(self):
        self.db.connect()
        self.logger.info("Clearing user table")
        peewee_models.User.drop_table(True, True)
        #self.db.create_tables([peewee_models.User], safe=True)
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
        wbtnWhiskey = None
        self.db.connect()
        try:
            whiskey = peewee_models.Whiskey.get(peewee_models.Whiskey.name == name)
            wbtnWhiskey = models.Whiskey(whiskeyId=whiskey.id, name=whiskey.name, price=whiskey.price, proof=whiskey.proof, style=whiskey.style, age=whiskey.age, icon=whiskey.icon, createdTime=whiskey.createdTime, lastUpdatedTime=whiskey.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnWhiskey

    def getWhiskeyById(self, whiskeyId):
        '''Lookup whiskey by ID'''
        wbtnWhiskey = None
        self.db.connect()
        try:
            whiskey = peewee_models.Whiskey.get(peewee_models.Whiskey.id == whiskeyId)
            wbtnWhiskey = models.Whiskey(whiskeyId=whiskey.id, name=whiskey.name, price=whiskey.price, proof=whiskey.proof, style=whiskey.style, age=whiskey.age, icon=whiskey.icon, createdTime=whiskey.createdTime, lastUpdatedTime=whiskey.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnWhiskey
    
    def getAllWhiskies(self, currentPage, itemsPerPage, sortField='name'):
        ''' Get all whiskies - paged.  First page returned is 1 (not 0)'''
        self.logger.debug("Requesting page %d from allUsers", currentPage)
        # Cap itemsPerPage at 100
        if itemsPerPage > 100:
            self.logger.warn("Requested %d itemsPerPage exceeded max of 100", itemsPerPage)
            itemsPerPage = 100
            
        sf = None
        if   sortField == 'name'  : sf = peewee_models.Whiskey.name
        elif sortField == 'price' : sf = peewee_models.Whiskey.price
        elif sortField == 'proof' : sf = peewee_models.Whiskey.proof
        elif sortField == 'style' : sf = peewee_models.Whiskey.style
        elif sortField == 'age'   : sf = peewee_models.Whiskey.age
        else : sf = peewee_models.Whiskey.name
            
        whiskies = []
        self.db.connect()
        for whiskey in peewee_models.Whiskey.select(peewee_models.Whiskey.name,
                                              peewee_models.Whiskey.price,
                                              peewee_models.Whiskey.proof,
                                              peewee_models.Whiskey.style,
                                              peewee_models.Whiskey.age,
                                              peewee_models.Whiskey.icon).order_by(sf).paginate(currentPage, itemsPerPage):
            whiskies.append(model_to_dict(whiskey))
        self.db.close
        
        self.logger.debug("Returning whiskies: %s", simplejson.dumps(whiskies))
        
        return simplejson.dumps(whiskies)

    def deleteWhiskeyByName(self, name):
        '''Delete a whiskey by name'''
        self.db.connect()
        self.logger.info("Deleteing whiskey %s", name)
        
        try:
            with self.db.transaction():
                query = peewee_models.Whiskey.delete().where(peewee_models.Whiskey.name == name)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete whiskey %s", name)
            self.db.close
            raise
        
        self.db.close

    def deleteWhiskeyById(self, whiskeyId):
        '''Delete a whiskey by whiskeyId'''
        self.db.connect()
        self.logger.info("Deleteing whiskey %s", whiskeyId)
        
        try:
            with self.db.transaction():
                query = peewee_models.Whiskey.delete().where(peewee_models.Whiskey.id == whiskeyId)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete whiskey %d", whiskeyId)
            self.db.close
            raise
        
        self.db.close

    def clearWhiskeyTable(self):
        self.db.connect()
        self.logger.info("Clearing whiskey table")
        peewee_models.Whiskey.drop_table(True, True)
        #self.db.create_tables([peewee_models.Whiskey], safe=True)
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
        wbtnBlog = None
        self.db.connect()
        try:
            blog = peewee_models.BlogEntry.get(peewee_models.BlogEntry.title == title)
            wbtnBlog = models.BlogEntry(blogEntryId=blog.id, title=blog.title, userId=blog.id, text=blog.text, createdTime=blog.createdTime, lastUpdatedTime=blog.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnBlog

    def getBlogEntryById(self, blogEntryId):
        '''Lookup a blog entry by ID'''
        wbtnBlog = None
        self.db.connect()
        try:
            blog = peewee_models.BlogEntry.get(peewee_models.BlogEntry.id == blogEntryId)
            wbtnBlog = models.BlogEntry(blogEntryId=blog.id, title=blog.title, userId=blog.id, text=blog.text, createdTime=blog.createdTime, lastUpdatedTime=blog.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnBlog

    def deleteBlogEntryByTitle(self, title):
        '''Delete a blog entry by title'''
        self.db.connect()
        self.logger.info("Deleteing blog entry %s", title)
        
        try:
            with self.db.transaction():
                query = peewee_models.BlogEntry.delete().where(peewee_models.BlogEntry.title == title)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete blog entry %s", title)
            self.db.close
            raise
        
        self.db.close

    def deleteBlogEntryById(self, blogEntryId):
        '''Delete a blog entry by blogEntryId'''
        self.db.connect()
        self.logger.info("Deleteing blog entry %s", blogEntryId)
        
        try:
            with self.db.transaction():
                query = peewee_models.BlogEntry.delete().where(peewee_models.BlogEntry.id == blogEntryId)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete blog entry %d", blogEntryId)
            self.db.close
            raise
        
        self.db.close

    def clearBlogEntryTable(self):
        self.db.connect()
        self.logger.info("Clearing blog entry table")
        peewee_models.BlogEntry.drop_table(True)
        #self.db.create_tables([peewee_models.BlogEntry], safe=True)
        self.db.close

    #############################################
    ##
    ##
    ##  Methods for CalculatedScore table
    ##
    ##
    #############################################

    def addCalculatedScore(self, whiskeyId, score, value, drinkability, complexity, mouthfeel):
        '''Add a new calculated score to the database.  This table is bound to the whiskeyId'''
        try:
            self.db.connect()
            with self.db.transaction():
                peewee_models.CalculatedScore.create(
                    whiskeyId=whiskeyId,
                    score=score,
                    value=value,
                    drinkability=drinkability,
                    complexity=complexity,
                    mouthfeel=mouthfeel,
                    createdTime=datetime.datetime.now(),
                    lastUpdatedTime=datetime.datetime.now())
            self.db.close

        except IntegrityError:
            self.logger.error("Failed to add calculated score %s, score for this whiskeyId is already present", whiskeyId)
            self.db.close
            raise
        
    def getCalculatedScoreByWhiskeyId(self, whiskeyId):
        '''Lookup a calculated score by whiskeyId'''
        wbtnScore = None
        self.db.connect()
        try:
            score = peewee_models.CalculatedScore.get(peewee_models.CalculatedScore.whiskeyId == whiskeyId)
            wbtnScore = models.CalculatedScore(whiskeyId=score.whiskeyId, score=score.score, value=score.value, drinkability=score.drinkability, complexity=score.complexity, mouthfeel=score.mouthfeel, createdTime=score.createdTime, lastUpdatedTime=score.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnScore

    def getCalculatedScoreByWhiskeyName(self, name):
        '''Lookup a calculated score by whiskey name'''
        wbtnScore = None
        self.db.connect()
        try:
            whiskey = peewee_models.Whiskey.get(peewee_models.Whiskey.name == name)
            score = peewee_models.CalculatedScore.get(peewee_models.CalculatedScore.whiskeyId == whiskey.id)
            wbtnScore = models.CalculatedScore(whiskeyId=score.whiskeyId, score=score.score, value=score.value, drinkability=score.drinkability, complexity=score.complexity, mouthfeel=score.mouthfeel, createdTime=score.createdTime, lastUpdatedTime=score.lastUpdatedTime)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnScore

    def deleteCalculatedScoreByWhiskeyId(self, whiskeyId):
        '''Delete a calculated score by whiskeyId'''
        self.db.connect()
        self.logger.info("Deleteing calculated score for whiskey %s", whiskeyId)
        
        try:
            with self.db.transaction():
                query = peewee_models.CalculatedScore.delete().where(peewee_models.CalculatedScore.whiskeyId == whiskeyId)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete calculated score for whiskey %d", whiskeyId)
            self.db.close
            raise
        
        self.db.close

    def clearCalculatedScoreTable(self):
        self.db.connect()
        self.logger.info("Clearing calculated score table")
        peewee_models.CalculatedScore.drop_table(True)
        #self.db.create_tables([peewee_models.CalculatedScore], safe=True)
        self.db.close
        
    #############################################
    ##
    ##
    ##  Methods for UserRating table
    ##
    ##
    #############################################

    def addUserRating(self, whiskeyId, userId, rating, notes=None, sweet=None, sour=None, heat=None, smooth=None, finish=None, crisp=None, leather=None, wood=None, smoke=None, citrus=None, floral=None, fruit=None):
        '''Add a new user rating to the database.  This table is bound to the whiskeyId and userId'''
        try:
            self.db.connect()
            with self.db.transaction():
                peewee_models.UserRating.create(
                    whiskeyId=whiskeyId,
                    rating=rating,
                    notes=notes,
                    userId=userId,
                    sweet=sweet,
                    sour=sour,
                    heat=heat,
                    smooth=smooth,
                    finish=finish,
                    crisp=crisp,
                    leather=leather,
                    wood=wood,
                    smoke=smoke,
                    citrus=citrus,
                    floral=floral,
                    fruit=fruit,
                    createdTime=datetime.datetime.now(),
                    lastUpdatedTime=datetime.datetime.now())
            self.db.close

        except IntegrityError:
            self.logger.error("Failed to add user rating for whiskey %s by user %s, score for this whiskeyId is already present", whiskeyId, userId)
            self.db.close
            raise
        
    def getUserRatingByWhiskeyId(self, whiskeyId, userId):
        '''Lookup a user ratings by whiskeyId and userId'''
        wbtnRating = None
        self.db.connect()
        try:
            r = peewee_models.UserRating.get(peewee_models.UserRating.whiskeyId == whiskeyId, peewee_models.UserRating.userId == userId)
            wbtnRating = models.UserRating(whiskeyId=r.whiskeyId, userId=r.userId, rating=r.rating, createdTime=r.createdTime, lastUpdatedTime=r.lastUpdatedTime, notes=r.notes, sweet=r.sweet, sour=r.sour, heat=r.heat, smooth=r.smooth, finish=r.finish, crisp=r.crisp, leather=r.leather, wood=r.wood, smoke=r.smoke, citrus=r.citrus, floral=r.floral, fruit=r.fruit)
        except DoesNotExist:
            pass
        
        self.db.close
        return wbtnRating

    def deleteUserRatingByWhiskeyId(self, whiskeyId, userId):
        '''Delete a user rating by whiskeyId and userId'''
        self.db.connect()
        self.logger.info("Deleteing user rating for whiskey %s for user %s", whiskeyId, userId)
        
        try:
            with self.db.transaction():
                query = peewee_models.UserRating.delete().where(peewee_models.UserRating.whiskeyId == whiskeyId, peewee_models.UserRating.userId == userId)
                query.execute()
        except IntegrityError:
            self.logger.error("Failed to delete rating by user %d for whiskey %d", userId, whiskeyId)
            self.db.close
            raise
        
        self.db.close

    def clearUserRatingTable(self):
        self.db.connect()
        self.logger.info("Clearing user rating table")
        peewee_models.UserRating.drop_table(True)
        #self.db.create_tables([peewee_models.UserRating], safe=True)
        self.db.close
