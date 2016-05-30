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

class BlogEntry(BaseModel):
    userId = peewee.ForeignKeyField(User)
    title = peewee.CharField()
    text = peewee.TextField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class User(BaseModel):
    firstName = peewee.CharField()
    middleInitial = peewee.CharField()
    lastName = peewee.CharField()
    suffix = peewee.CharField()
    email = peewee.CharField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()
    icon = peewee.BlobField()
    userRater = peewee.BooleanField()
    blogWriter = peewee.BooleanField()
    collegeRater = peewee.BooleanField()
    whiskeyAdmin = peewee.BooleanField()

class UserRating(BaseModel):
    whiskeyId = peewee.ForeignKeyField(Whiskey)
    userId = peewee.ForeignKeyField(User)
    rating = peewee.FloatField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()
    notes = peewee.TextField()

class CalculatedScores(BaseModel):
    whiskeyId = peewee.ForeignKeyField(Whiskey)
    score = peewee.FloatField()
    value = peewee.FloatField()
    drinkability = peewee.FloatField()
    complexity = peewee.FloatField()
    mouthfeel = peewee.FloatField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class CollegeRating(BaseModel):
    whiskeyId = peewee.ForeignKeyField(Whiskey)
    userId = peewee.ForeignKeyField(User)
    sweet = peewee.FloatField()
    sour = peewee.FloatField()
    heat = peewee.FloatField()
    smooth = peewee.FloatField() 
    finish = peewee.FloatField()
    crisp = peewee.FloatField()
    leather = peewee.FloatField()
    wood = peewee.FloatField()
    smoke = peewee.FloatField()
    citrus = peewee.FloatField()
    floral = peewee.FloatField()
    fruit = peewee.FloatField()
    notes = peewee.TextField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class Whiskey(BaseModel):
    name = peewee.CharField()
    price = peewee.FloatField()
    proof = peewee.FloatField()
    style = peewee.CharField()
    age = peewee.IntegerField()
    icon = peewee.BlobField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

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
