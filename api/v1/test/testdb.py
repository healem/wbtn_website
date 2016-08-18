#!../../bin/python
import unittest
import datetime
from utils import loginit
from db import datastore
from db.peewee_wbtn import peewee_models
from peewee import IntegrityError, DoesNotExist
from freezegun import freeze_time
    
class DBTest(unittest.TestCase):

    dbm = None

    @classmethod
    def setUpClass(cls):
        loginit.initTestLogging()
        
        '''Temp db instance to clear out any garbage'''
        DBTest.d = datastore.DbManager(testMode=True)
        DBTest.d.clearUserRatingTable()
        DBTest.d.clearCalculatedScoreTable()
        DBTest.d.clearBlogEntryTable()
        DBTest.d.clearWhiskeyTable()
        DBTest.d.clearUserTable()
        '''Now create the instance that we will use for the rest of the test'''
        DBTest.dbm = datastore.DbManager(testMode=True)

    @classmethod
    def tearDownClass(cls):
        pass
        #DBTest.dbm.clearUserRatingTable()
        #DBTest.dbm.clearCalculatedScoreTable()
        #DBTest.dbm.clearBlogEntryTable()
        #DBTest.dbm.clearWhiskeyTable()
        #DBTest.dbm.clearUserTable()

    def test_init(self):
        for table in self.dbm.wbtnTables:
            self.assertTrue(table.table_exists)

    def test_addNormalUser(self):
        testEmail = "test@dmjkg.com"
        testFirst = "sfdgjnk"
        testMI = "SIOH"
        testLast = "sdharhIoiu"
        testSuffix = "sdfhas"
        testIcon = bytearray("ashdkgfualesbsbvlansufbalsug")
        testFBID = "438q5697-816058-9y304587-039485"
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()

        te1 = "testdsjkhg@jhglsg.asfg.edu"

        '''Basic case'''
        self.dbm.addNormalUser(email=testEmail)
        eu = self.dbm.getUserByEmail(testEmail)
        self.assertEqual(eu.email, testEmail)
        self.assertTrue(eu.userRater)
        self.assertFalse(eu.blogWriter)
        self.assertFalse(eu.collegeRater)
        self.assertFalse(eu.whiskeyAdmin)
        self.assertIsNone(eu.facebookId)
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addNormalUser(email=te1, facebookId=testFBID, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu1 = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu1.email, te1)
        self.assertEqual(eu1.facebookId, testFBID)
        self.assertTrue(eu1.userRater)
        self.assertFalse(eu1.blogWriter)
        self.assertFalse(eu1.collegeRater)
        self.assertFalse(eu1.whiskeyAdmin)
        self.assertEqual(eu1.firstName, testFirst)
        self.assertEqual(eu1.lastName, testLast)
        self.assertEqual(eu1.middleInitial, testMI)
        self.assertEqual(eu1.suffix, testSuffix)
        self.assertEqual(eu1.icon, testIcon)
        self.assertEqual(eu1.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu1.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        

        '''Get user by ID'''
        eu2 = self.dbm.getUserById(eu1.userId)
        self.assertEqual(eu1.email, eu2.email)
        
        '''Add facebook id to existing user'''
        self.dbm.addFacebookAccountToUser(eu.userId, testFBID)
        eu3 = self.dbm.getUserById(eu.userId)
        self.assertEqual(eu3.facebookId, testFBID)
        
        '''Add facebook account to non-existing user'''
        with self.assertRaises(DoesNotExist):
            self.dbm.addFacebookAccountToUser(eu1.userId + 10, testFBID)

        '''Email address taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addNormalUser(email=testEmail)

        '''User does not exist, lookup by email'''
        self.assertIsNone(self.dbm.getUserByEmail(email="does@not.exist"))
        
        '''User does not exist, lookup by ID'''
        self.assertIsNone(self.dbm.getUserById(userId=3457))

        '''Delete user by email'''
        self.dbm.deleteUserByEmail(te1)
        self.assertIsNone(self.dbm.getUserByEmail(email=te1))

        '''Delete user by ID'''
        self.dbm.deleteUserById(eu.userId)
        self.assertIsNone(self.dbm.getUserById(eu.userId))

    def test_addBlogWriterUser(self):
        testEmail = "bwtest@dmjkg.com"
        testFirst = "bwsfdgjnk"
        testMI = "bwSIOH"
        testLast = "bwsdharhIoiu"
        testSuffix = "bwsdfhas"
        testFBID = "438q5697-816368-9y304587-039485"
        testIcon = bytearray("bwashdkgfualesbsbvlansufbalsug")
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()

        te1 = "bwtestdsjkhg@jhglsg.asfg.edu"

        '''Basic case'''
        self.dbm.addBlogWriterUser(email=testEmail)
        eu = self.dbm.getUserByEmail(testEmail)
        self.assertEqual(eu.email, testEmail)
        self.assertTrue(eu.userRater)
        self.assertTrue(eu.blogWriter)
        self.assertFalse(eu.collegeRater)
        self.assertFalse(eu.whiskeyAdmin)
        self.assertIsNone(eu.facebookId)
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addBlogWriterUser(email=te1, facebookId=testFBID, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
        self.assertEqual(eu.facebookId, testFBID)
        self.assertTrue(eu.userRater)
        self.assertTrue(eu.blogWriter)
        self.assertFalse(eu.collegeRater)
        self.assertFalse(eu.whiskeyAdmin)
        self.assertEqual(eu.firstName, testFirst)
        self.assertEqual(eu.lastName, testLast)
        self.assertEqual(eu.middleInitial, testMI)
        self.assertEqual(eu.suffix, testSuffix)
        self.assertEqual(eu.icon, testIcon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Email address taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addBlogWriterUser(email=testEmail)

    def test_addCollegeRaterUser(self):
        testEmail = "crtest@dmjkg.com"
        testFirst = "crsfdgjnk"
        testMI = "crSIOH"
        testLast = "crsdharhIoiu"
        testSuffix = "crsdfhas"
        testFBID = "438q5697-816058-9y30454767-039485"
        testIcon = bytearray("crashdkgfualesbsbvlansufbalsug")
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()

        te1 = "crtestdsjkhg@jhglsg.asfg.edu"

        '''Basic case'''
        self.dbm.addCollegeRaterUser(email=testEmail)
        eu = self.dbm.getUserByEmail(testEmail)
        self.assertEqual(eu.email, testEmail)
        self.assertTrue(eu.userRater)
        self.assertFalse(eu.blogWriter)
        self.assertTrue(eu.collegeRater)
        self.assertFalse(eu.whiskeyAdmin)
        self.assertIsNone(eu.facebookId)
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addCollegeRaterUser(email=te1, facebookId=testFBID, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
        self.assertEqual(eu.facebookId, testFBID)
        self.assertTrue(eu.userRater)
        self.assertFalse(eu.blogWriter)
        self.assertTrue(eu.collegeRater)
        self.assertFalse(eu.whiskeyAdmin)
        self.assertEqual(eu.firstName, testFirst)
        self.assertEqual(eu.lastName, testLast)
        self.assertEqual(eu.middleInitial, testMI)
        self.assertEqual(eu.suffix, testSuffix)
        self.assertEqual(eu.icon, testIcon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Email address taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addCollegeRaterUser(email=testEmail)

    def test_addWhiskeyAdminUser(self):
        testEmail = "watest@dmjkg.com"
        testFirst = "wasfdgjnk"
        testMI = "waSIOH"
        testLast = "wasdharhIoiu"
        testSuffix = "wasdfhas"
        testFBID = "438q5697-816058-9y304587-039486947"
        testIcon = bytearray("waashdkgfualesbsbvlansufbalsug")
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()

        te1 = "watestdsjkhg@jhglsg.asfg.edu"

        '''Basic case'''
        self.dbm.addWhiskeyAdminUser(email=testEmail)
        eu = self.dbm.getUserByEmail(testEmail)
        self.assertEqual(eu.email, testEmail)
        self.assertTrue(eu.userRater)
        self.assertTrue(eu.blogWriter)
        self.assertTrue(eu.collegeRater)
        self.assertTrue(eu.whiskeyAdmin)
        self.assertIsNone(eu.facebookId)
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addWhiskeyAdminUser(email=te1, facebookId=testFBID, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
        self.assertEqual(eu.facebookId, testFBID)
        self.assertTrue(eu.userRater)
        self.assertTrue(eu.blogWriter)
        self.assertTrue(eu.collegeRater)
        self.assertTrue(eu.whiskeyAdmin)
        self.assertEqual(eu.firstName, testFirst)
        self.assertEqual(eu.lastName, testLast)
        self.assertEqual(eu.middleInitial, testMI)
        self.assertEqual(eu.suffix, testSuffix)
        self.assertEqual(eu.icon, testIcon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Email address taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addWhiskeyAdminUser(email=testEmail)
            
    def test_addWhiskey(self):
        tname1 = "Test Whiskey 1"
        tname2 = "Test Whiskey 2"
        tprice = 35.00
        tproof = 80
        tage = 18
        ticon = bytearray("waashdkgfualesbsbvlansufbalsug")
        tstyle = "Bourbon"
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        
        '''Basic case'''
        self.dbm.addWhiskey(name=tname1)
        w = self.dbm.getWhiskeyByName(tname1)
        self.assertEqual(w.name, tname1)
        self.assertIsNone(w.price)
        self.assertIsNone(w.proof)
        self.assertIsNone(w.age)
        self.assertIsNone(w.icon)
        self.assertIsNone(w.style)
        self.assertEqual(w.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(w.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''Normal case'''
        self.dbm.addWhiskey(name=tname2, price=tprice, proof=tproof, age=tage, icon=ticon, style=tstyle)
        w1 = self.dbm.getWhiskeyByName(tname2)
        self.assertEqual(w1.name, tname2)
        self.assertEqual(w1.price, tprice)
        self.assertEqual(w1.proof, tproof)
        self.assertEqual(w1.age, tage)
        self.assertEqual(w1.icon, ticon)
        self.assertEqual(w1.style, tstyle)
        self.assertEqual(w1.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(w1.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''Whiskey name taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addWhiskey(name=tname1)
            
        '''Get whiskey by id'''
        w2 = self.dbm.getWhiskeyById(w1.whiskeyId)
        self.assertEqual(w1.name, w2.name)
        
        '''Whiskey does not exist'''
        self.assertIsNone(self.dbm.getWhiskeyByName(name="doesnotexist"))

        '''Delete Whiskey by name'''
        self.dbm.deleteWhiskeyByName(tname2)
        self.assertIsNone(self.dbm.getWhiskeyByName(name=tname2))

        '''Delete Whiskey by ID'''
        self.dbm.deleteWhiskeyById(w1.whiskeyId)
        self.assertIsNone(self.dbm.getWhiskeyById(w1.whiskeyId))
            
    def test_addBlogEntry(self):
        tt1 = "Title 1"
        tt2 = "Title 2"
        ttext = "alsighiua alrhgl uasryt8 ag4rtl7awg tugabwrf7b 8w4b47abv a8ui lrbfausl fgaebrfgwtgf agerg"
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        testEmail = "agkyrgtalb@jkblzdfg.com"
        
        '''Create user for testing'''
        self.dbm.addNormalUser(email=testEmail)
        tu = self.dbm.getUserByEmail(testEmail)
        
        '''Normal case'''
        self.dbm.addBlogEntry(title=tt1, text=ttext, userId=tu.userId)
        b = self.dbm.getBlogEntryByTitle(tt1)
        self.assertEqual(b.title, tt1)
        self.assertEqual(b.text, ttext)
        self.assertEqual(b.userId, tu.userId)
        self.assertEqual(b.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(b.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''Blog entry title taken taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addBlogEntry(title=tt1, text=ttext, userId=tu.userId)
            
        '''Get Blog Entry by id'''
        b1 = self.dbm.getBlogEntryById(b.blogEntryId)
        self.assertEqual(b.title, b1.title)
        
        '''Blog entry does not exist'''
        self.assertIsNone(self.dbm.getBlogEntryByTitle(title="doesnotexist"))

        '''Delete blog entry by title'''
        self.dbm.addBlogEntry(title=tt2, text=ttext, userId=tu.userId)
        b2 = self.dbm.getBlogEntryByTitle(tt2)
        self.assertEqual(b2.title, tt2)
        self.dbm.deleteBlogEntryByTitle(tt2)
        self.assertIsNone(self.dbm.getBlogEntryByTitle(title=tt2))

        '''Delete blog entry by ID'''
        self.dbm.deleteBlogEntryById(b1.blogEntryId)
        self.assertIsNone(self.dbm.getBlogEntryById(b1.blogEntryId))
            
    def test_addCalculatedScore(self):
        tname1 = "Test Whiskey 11"
        tname2 = "Test Whiskey 12"
        tprice = 35.00
        tproof = 80
        tage = 18
        ticon = bytearray("waashdkgfualesbsbvlansufbalsug")
        tstyle = "Bourbon"
        
        score = 3.75
        value = 2.50
        drink = 4.25
        comp = 4.32
        mf = 4.13
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        
        '''Create test whiskies'''
        self.dbm.addWhiskey(name=tname1, price=tprice, proof=tproof, age=tage, icon=ticon, style=tstyle)
        self.dbm.addWhiskey(name=tname2, price=tprice, proof=tproof, age=tage, icon=ticon, style=tstyle)
        w1 = self.dbm.getWhiskeyByName(tname1)
        w2 = self.dbm.getWhiskeyByName(tname2)
        
        '''Normal case'''
        self.dbm.addCalculatedScore(whiskeyId=w1.whiskeyId, score=score, value=value, drinkability=drink, complexity=comp, mouthfeel=mf)
        self.dbm.addCalculatedScore(whiskeyId=w2.whiskeyId, score=score, value=value, drinkability=drink, complexity=comp, mouthfeel=mf)
        s = self.dbm.getCalculatedScoreByWhiskeyId(w1.whiskeyId)
        self.assertEqual(s.score, score)
        self.assertEqual(s.value, value)
        self.assertEqual(s.drinkability, drink)
        self.assertEqual(s.complexity, comp)
        self.assertEqual(s.mouthfeel, mf)
        self.assertEqual(s.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(s.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''Calculated score already exists for whiskey'''
        with self.assertRaises(IntegrityError):
            self.dbm.addCalculatedScore(whiskeyId=w1.whiskeyId, score=score, value=value, drinkability=drink, complexity=comp, mouthfeel=mf)
            
        '''Get CalculatedScore by Whiskey name'''
        s1 = self.dbm.getCalculatedScoreByWhiskeyName(w1.name)
        self.assertEqual(s1.whiskeyId.id, w1.whiskeyId)
        self.assertEqual(s1.score, score)
        
        '''Calculated score does not exist, by whiskeyId'''
        self.assertIsNone(self.dbm.getCalculatedScoreByWhiskeyId(whiskeyId=999))
            
        '''Calculated score does not exist, by whiskey name'''
        self.assertIsNone(self.dbm.getCalculatedScoreByWhiskeyName(name="doesnotexist"))

        '''Delete calculate score by whiskeyId'''
        self.dbm.deleteCalculatedScoreByWhiskeyId(w1.whiskeyId)
        self.assertIsNone(self.dbm.getCalculatedScoreByWhiskeyId(whiskeyId=w1.whiskeyId))
            
    def test_addUserRating(self):
        ''' Test whiskey '''
        tname1 = "Test Whiskey 21"
        tname2 = "Test Whiskey 22"
        tprice = 35.00
        tproof = 80
        tage = 18
        ticon = bytearray("waashdkgfualesbsbvlansufbalsug")
        tstyle = "Bourbon"
        
        ''' Test user '''
        te1 = "testdsjkhg21@jhglsg.asfg.edu"
        te2 = "test22@dmjkg.com"
        testFirst = "sfdgjnk"
        testMI = "SIOH"
        testLast = "sdharhIoiu"
        testSuffix = "sdfhas"
        testFBID1 = "43823597-816058-9y304587-039486947"
        testFBID2 = "4386579697-816058-9y304587-039486947"
        testIcon = bytearray("ashdkgfualesbsbvlansufbalsug")
        
        ''' Test rating '''
        trating = 3.00
        tsweet = 4.25
        tsour = 3.75
        theat = 2.00
        tsmooth = 2.00
        tfinish = 1.75
        tcrisp = 1.00
        tleather = 5.00
        twood = 4.75
        tsmoke = 2.00
        tcitrus = 4.00
        tfloral = 3.00
        tfruit = 3.00
        tnotes = "asiugba7oebgiuWB78VBA E87QG 78OQBW8YRFB IA8WBRFOGABUYERGBLAWR"
        
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        
        '''Create test whiskies'''
        self.dbm.addWhiskey(name=tname1, price=tprice, proof=tproof, age=tage, icon=ticon, style=tstyle)
        self.dbm.addWhiskey(name=tname2, price=tprice, proof=tproof, age=tage, icon=ticon, style=tstyle)
        w1 = self.dbm.getWhiskeyByName(tname1)
        w2 = self.dbm.getWhiskeyByName(tname2)
        
        '''Create test users'''
        self.dbm.addNormalUser(email=te1, facebookId=testFBID1, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        self.dbm.addNormalUser(email=te2, facebookId=testFBID2, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        u1 = self.dbm.getUserByEmail(te1)
        u2 = self.dbm.getUserByEmail(te2)
        
        '''Simple case'''
        self.dbm.addUserRating(whiskeyId=w1.whiskeyId, userId=u1.userId, rating=trating, notes=tnotes)
        r1 = self.dbm.getUserRatingByWhiskeyId(w1.whiskeyId, u1.userId)
        self.assertEqual(r1.rating, trating)
        self.assertEqual(r1.notes, tnotes)
        self.assertEqual(r1.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(r1.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''College rater case'''
        self.dbm.addUserRating(whiskeyId=w2.whiskeyId, userId=u2.userId, rating=trating, notes=tnotes, sweet=tsweet, sour=tsour, heat=theat, smooth=tsmooth, finish=tfinish, crisp=tcrisp, leather=tleather, wood=twood, smoke=tsmoke, citrus=tcitrus, floral=tfloral, fruit=tfruit)
        r2 = self.dbm.getUserRatingByWhiskeyId(w2.whiskeyId, u2.userId)
        self.assertEqual(r2.rating, trating)
        self.assertEqual(r2.notes, tnotes)
        self.assertEqual(r2.sweet, tsweet)
        self.assertEqual(r2.sour, tsour)
        self.assertEqual(r2.heat, theat)
        self.assertEqual(r2.smooth, tsmooth)
        self.assertEqual(r2.finish, tfinish)
        self.assertEqual(r2.crisp, tcrisp)
        self.assertEqual(r2.leather, tleather)
        self.assertEqual(r2.wood, twood)
        self.assertEqual(r2.smoke, tsmoke)
        self.assertEqual(r2.citrus, tcitrus)
        self.assertEqual(r2.floral, tfloral)
        self.assertEqual(r2.fruit, tfruit)
        self.assertEqual(r2.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(r2.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        
        '''User rating already exists for whiskey'''
        with self.assertRaises(IntegrityError):
            self.dbm.addUserRating(whiskeyId=w1.whiskeyId, userId=u1.userId, rating=trating, notes=tnotes)
            
        '''User rating does not exist, by whiskey id'''
        self.assertIsNone(self.dbm.getUserRatingByWhiskeyId(w2.whiskeyId, u1.userId))

        '''Delete user rating by whiskeyId'''
        self.dbm.deleteUserRatingByWhiskeyId(w1.whiskeyId, u1.userId)
        self.assertIsNone(self.dbm.getUserRatingByWhiskeyId(w1.whiskeyId, u1.userId))
    

# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
