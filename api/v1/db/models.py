#!../../bin/python

class User():

    def __init__(self, userId, email, createdTime, userRater, blogWriter, collegeRater, whiskeyAdmin, firstName=None, middleInitial=None, lastName=None, suffix=None, lastUpdatedTime=None, icon=None):
        self.userId = userId
        self.firstName = firstName
        self.middleInitial = middleInitial
        self.lastName = lastName
        self.suffix = suffix
        self.email = email
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime
        self.icon = icon
        self.userRater = userRater
        self.blogWriter = blogWriter
        self.collegeRater = collegeRater
        self.whiskeyAdmin = whiskeyAdmin

class Whiskey():

    def __init__(self, whiskeyId, name, createdTime, price=None, proof=None, style=None, age=None, icon=None, lastUpdatedTime=None):
        self.whiskeyId = whiskeyId
        self.name = name
        self.price = price
        self.proof = proof
        self.style = style
        self.age = age
        self.icon = icon
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime

class BlogEntry():

    def __init__(self, blogEntryId, userId, title, text, createdTime, lastUpdatedTime=None):
        self.blogEntryId = blogEntryId
        self.userId = userId
        self.title = title
        self.text = text
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime

class UserRating():

    def __init__(self, whiskeyId, userId, rating, createdTime, lastUpdatedTime=None, notes=None, sweet=None, sour=None, heat=None, smooth=None, finish=None, crisp=None, leather=None, wood=None, smoke=None, citrus=None, floral=None, fruit=None):
        self.whiskeyId = whiskeyId
        self.userId = userId
        self.rating = rating
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime
        self.notes = notes
        self.sweet = sweet
        self.sour = sour
        self.heat = heat
        self.smooth = smooth
        self.finish = finish
        self.crisp = crisp
        self.leather = leather
        self.wood = wood
        self.smoke = smoke
        self.citrus = citrus
        self.floral = floral
        self.fruit = fruit

class CalculatedScore():

    def __init__(self, whiskeyId, score, value, drinkability, complexity, mouthfeel, createdTime, lastUpdatedTime=None):
        self.whiskeyId = whiskeyId
        self.score = score
        self.value = value
        self.drinkability = drinkability
        self.complexity = complexity
        self.mouthfeel = mouthfeel
        self.createdTime = createdTime
        self.lastUpdatedTime = lastUpdatedTime
