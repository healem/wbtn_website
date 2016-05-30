#!../../bin/python

import peewee
import ConfigParser
from playhouse.shortcuts import RetryOperationalError
configFile = "/home4/healem/keys/wbtn.cnf"

config = ConfigParser.ConfigParser()
config.read(configFile)
userName = "healem_wbtn"
readPw = config.get("db", userName)

dbName = "healem_wbtn"

class WBTNDB(RetryOperationalError, peewee.MySQLDatabase):
    pass

db = WBTNDB(None)
class BaseModel(peewee.Model):

    class Meta:
        database = db

class BlogEntry(WBTNDB):
    userId = peewee.ForeignKeyField(User)
    title = peewee.TextField()
    text = peewee.TextField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class User(WBTNDB):
    firstName = peewee.CharField()
    middleInitial = peewee.CharField()
    lastName = peewee.CharField()
    suffix = peewee.CharField()
    email = peewee.CharField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()
    icon = peewee.BlobField()

class Test(BaseModel):
    testName = peewee.CharField()

if __name__ == "__main__":
    try:
        db.init(dbName, user=userName, passwd=readPw)
        db.connect()
        db.create_tables([Test])
        #db.create_tables([Test], safe=True)
        db.close()
    except peewee.OperationalError:
        print "Test table already exists!"
