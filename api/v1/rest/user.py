#!../../bin/python
import logging
from flask_restplus import Resource, Namespace

api = Namespace('user', description='User related operations')

user = api.model('User', {
    'userId': fields.String(required=True, description='The user identifier'),
    'email': fields.String(required=True, description='The email address of the user'),
    'firstName': fields.String(required=False, description='User first name'),
    'lastName': fields.String(required=False, description='User last name'),
    'createdTime': fields.DateTime(required=True, description='When the user was created'),
    'lastUpdatedTime': fields.DateTime(required=True, description='The last time the user profile was updated'),
    'userRater': fields.Boolean(required=True, description='User has permission to rate whiskies'),
    'blogWriter': fields.Boolean(required=True, description='User has permission to create blog posts'),
    'collegeRater': fields.Boolean(required=True, description='User has permission to create advanced ratings'),
    'whiskeyAdmin': fields.Boolean(required=True, description='User is an admin'),
})
