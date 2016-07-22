#!../../bin/python

import peewee
import ConfigParser
from playhouse.shortcuts import RetryOperationalError
configFile = "/home4/healem/keys/wbtn.cnf"

config = ConfigParser.ConfigParser()
config.read(configFile)
userName = "healem_wbtn"
readPw = config.get("db", userName)

dbName = "healem_wbtn_test"

class WBTNDB(RetryOperationalError, peewee.MySQLDatabase):
    pass

class BaseModel(peewee.Model):

    @classmethod
    def getDbRef(cls):
        return cls._meta.database

    class Meta:
        database = WBTNDB(None)

class User(BaseModel):
    firstName = peewee.CharField(null=True)
    middleInitial = peewee.CharField(null=True)
    lastName = peewee.CharField(null=True)
    suffix = peewee.CharField(null=True)
    email = peewee.CharField(unique=True)
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()
    icon = peewee.BlobField(null=True)
    userRater = peewee.BooleanField()
    blogWriter = peewee.BooleanField()
    collegeRater = peewee.BooleanField()
    whiskeyAdmin = peewee.BooleanField()

class Whiskey(BaseModel):
    name = peewee.CharField(unique=True)
    price = peewee.FloatField(null=True)
    proof = peewee.FloatField(null=True)
    style = peewee.CharField(null=True)
    age = peewee.IntegerField(null=True)
    icon = peewee.BlobField(null=True)
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()
    
    # TODO: add index of id and name

class BlogEntry(BaseModel):
    userId = peewee.ForeignKeyField(User)
    title = peewee.CharField(unique=True)
    text = peewee.TextField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class CalculatedScore(BaseModel):
    whiskeyId = peewee.ForeignKeyField(Whiskey, unique=True, primary_key=True)
    score = peewee.FloatField()
    value = peewee.FloatField()
    drinkability = peewee.FloatField()
    complexity = peewee.FloatField()
    mouthfeel = peewee.FloatField()
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

class UserRating(BaseModel):
    whiskeyId = peewee.ForeignKeyField(Whiskey)
    userId = peewee.ForeignKeyField(User)
    rating = peewee.FloatField()
    sweet = peewee.FloatField(null=True)
    sour = peewee.FloatField(null=True)
    heat = peewee.FloatField(null=True)
    smooth = peewee.FloatField(null=True)
    finish = peewee.FloatField(null=True)
    crisp = peewee.FloatField(null=True)
    leather = peewee.FloatField(null=True)
    wood = peewee.FloatField(null=True)
    smoke = peewee.FloatField(null=True)
    citrus = peewee.FloatField(null=True)
    floral = peewee.FloatField(null=True)
    fruit = peewee.FloatField(null=True)
    notes = peewee.TextField(null=True)
    createdTime = peewee.DateTimeField()
    lastUpdatedTime = peewee.DateTimeField()

    class Meta:
        primary_key = peewee.CompositeKey('whiskeyId', 'userId')

