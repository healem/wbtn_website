#!../bin/python
from utils import loginit
from db import datastore
    
loginit.initLogging()    
dbm = datastore.DbManager(testMode=True)
