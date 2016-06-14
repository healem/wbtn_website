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
        DBTest.dbm = datastore.DbManager(testMode=True)
        DBTest.dbm.clearUserTable()
        DBTest.dbm.clearWhiskeyTable()

    @classmethod
    def tearDownClass(cls):
        DBTest.dbm.clearUserTable()
        DBTest.dbm.clearWhiskeyTable()

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
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addNormalUser(email=te1, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu1 = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu1.email, te1)
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

        '''Email address taken'''
        with self.assertRaises(IntegrityError):
            self.dbm.addNormalUser(email=testEmail)

        '''User does not exist'''
        with self.assertRaises(DoesNotExist):
            self.dbm.getUserByEmail(email="does@not.exist")

        '''Delete user by email'''
        self.dbm.deleteUserByEmail(te1)
        with self.assertRaises(DoesNotExist):
            self.dbm.getUserByEmail(email=te1)

        '''Delete user by ID'''
        self.dbm.deleteUserById(eu.userId)
        with self.assertRaises(DoesNotExist):
            self.dbm.getUserById(eu.userId)

    def test_addBlogWriterUser(self):
        testEmail = "bwtest@dmjkg.com"
        testFirst = "bwsfdgjnk"
        testMI = "bwSIOH"
        testLast = "bwsdharhIoiu"
        testSuffix = "bwsdfhas"
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
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addBlogWriterUser(email=te1, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
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
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addCollegeRaterUser(email=te1, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
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
        self.assertIsNone(eu.firstName)
        self.assertIsNone(eu.lastName)
        self.assertIsNone(eu.middleInitial)
        self.assertIsNone(eu.suffix)
        self.assertIsNone(eu.icon)
        self.assertEqual(eu.createdTime, datetime.datetime(2012, 1, 14, 12, 0, 1))
        self.assertEqual(eu.lastUpdatedTime, datetime.datetime(2012, 1, 14, 12, 0, 1))

        '''Normal case'''
        self.dbm.addWhiskeyAdminUser(email=te1, firstName=testFirst, middleInitial=testMI, lastName=testLast, suffix=testSuffix, icon=testIcon)
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
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
        with self.assertRaises(DoesNotExist):
            self.dbm.getWhiskeyByName(name="doesnotexist")

        '''Delete Whiskey by name'''
        self.dbm.deleteWhiskeyByName(tname2)
        with self.assertRaises(DoesNotExist):
            self.dbm.getWhiskeyByName(name=tname2)

        '''Delete Whiskey by ID'''
        self.dbm.deleteWhiskeyById(w1.whiskeyId)
        with self.assertRaises(DoesNotExist):
            self.dbm.getWhiskeyById(w1.whiskeyId)
        
    

# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
