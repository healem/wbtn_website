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

    @classmethod
    def tearDownClass(cls):
        DBTest.dbm.clearUserTable()

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
        self.dbm.addNormalUser(email=testEmail, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None)
        eu = self.dbm.getUserByEmail(testEmail)
        self.assertEqual(eu.email, testEmail)
        #self.assertEqual(eu.id, 1)
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
        eu = self.dbm.getUserByEmail(te1)
        self.assertEqual(eu.email, te1)
        #self.assertEqual(eu.id, 2)
        self.assertTrue(eu.userRater)
        self.assertFalse(eu.blogWriter)
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
            self.dbm.addNormalUser(email=testEmail, firstName=None, middleInitial=None, lastName=None, suffix=None, icon=None)

        '''User does not exist'''
        with self.assertRaises(DoesNotExist):
            self.dbm.getUserByEmail(email="does@not.exist")

        '''Delete user'''
        self.dbm.deleteUserByEmail(te1)
        with self.assertRaises(DoesNotExist):
            self.dbm.getUserByEmail(email=te1)

# Necessary to be able to run the unit test
if (__name__ == '__main__'):
    unittest.main()
