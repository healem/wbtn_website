#!../bin/python
from utils import loginit
from db import datastore
    
loginit.initTestLogging()    
dbm = datastore.DbManager(testMode=True)
