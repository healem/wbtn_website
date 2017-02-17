#!../../../bin/python
import logging
import json
from flask import session
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from flask_restplus.inputs import boolean
from db import datastore
from ..restplus import api
from ..decorators import require_token, require_admin
from helpers import addRating, deleteRating, updateRating

logger = logging.getLogger("rating-routes")
ratingApi = Namespace('rating', description='Rating related operations')

rating = ratingApi.model('Rating', {
    'whiskeyId': fields.Integer(required=True, description='The ID of the whiskey'),
    'userId': fields.Integer(required=True, description='The ID of the user'),
    'rating': fields.Float(required=False, description='User rating of the whiskey'),
    'notes': fields.String(required=False, description='User note about the whiskey'),
    'sweet': fields.Float(required=False, description='Sweetness of the whiskey'),
    'sour': fields.Float(required=False, description='Sourness of the whiskey'),
    'heat': fields.Float(required=False, description='Hotness of the whiskey'),
    'smooth': fields.Float(required=False, description='Smoothness of the whiskey'),
    'finish': fields.Float(required=False, description='Finish of the whiskey'),
    'crisp': fields.Float(required=False, description='Crispness of the whiskey'),
    'leather': fields.Float(required=False, description='Leatheriness of the whiskey'),
    'wood': fields.Float(required=False, description='Woodiness of the whiskey'),
    'smoke': fields.Float(required=False, description='Smokeyness of the whiskey'),
    'citrus': fields.Float(required=False, description='Citrusness of the whiskey'),
    'floral': fields.Float(required=False, description='Floralness of the whiskey'),
    'fruit': fields.Float(required=False, description='Fruitiness of the whiskey'),
})

dbm = datastore.DbManager(testMode=False)

getAllParser = ratingApi.parser()
getAllParser.add_argument('currentPage', type=int, required=True, default=1, help='Current page of the query, count starts at 1')
getAllParser.add_argument('itemsPerPage', type=int, required=True, default=20, help='Number of items returned per page, max=100')
getAllParser.add_argument('sortField', type=str, required=False, default='whiskeyId', help='The name of the field to sort on: userId, whiskeyId, rating, wood, smoke, etc')

getParser = ratingApi.parser()
getParser.add_argument('whiskeyId', type=int, required=True, help='The ID of the whiskey')
getParser.add_argument('userId', type=int, required=True, help='The ID of the user')

ppParser = ratingApi.parser()
ppParser.add_argument('whiskeyId', type=int, required=True, help='The ID of the whiskey')
ppParser.add_argument('userId', type=int, required=True, help='The ID of the user')
ppParser.add_argument('rating', type=float, required=False, help='User rating of the whiskey')
ppParser.add_argument('notes', type=str, required=False, help='User note about the whiskey')
ppParser.add_argument('sweet', type=float, required=False, help='Sweetness of the whiskey')
ppParser.add_argument('sour', type=float, required=False, help='Sourness of the whiskey')
ppParser.add_argument('heat', type=float, required=False, help='Hotness of the whiskey')
ppParser.add_argument('smooth', type=float, required=False, help='Smoothness of the whiskey')
ppParser.add_argument('finish', type=float, required=False, help='Finish of the whiskey')
ppParser.add_argument('crisp', type=float, required=False, help='Crispness of the whiskey')
ppParser.add_argument('leather', type=float, required=False, help='Leatheriness of the whiskey')
ppParser.add_argument('wood', type=float, required=False, help='Woodiness of the whiskey')
ppParser.add_argument('smoke', type=float, required=False, help='Smokeyness of the whiskey')
ppParser.add_argument('citrus', type=float, required=False, help='Citrusness of the whiskey')
ppParser.add_argument('floral', type=float, required=False, help='Floralness of the whiskey')
ppParser.add_argument('fruit', type=float, required=False, help='Fruitiness of the whiskey')

@api.route('/allratings')
class WBTNRatings(Resource):
    @require_token
    @api.expect(getAllParser, True)
    def get(self):
        #logger.debug("Incoming request for all ratings")
        args = getAllParser.parse_args()
        #logger.debug("Getting all ratings with args: %s", args)
        allRatings = dbm.getAllRatings(args['currentPage'], args['itemsPerPage'], args['sortField'])
        #logger.debug("Returning allRatings: %s", allRatings)
        return allRatings
    
@api.route('/rating')
class WBTNRating(Resource):
    @require_token
    @api.expect(getParser)
    def get(self):
        args = getParser.parse_args()
        return getRating(args)
    
    @require_token
    @require_admin
    @api.expect(ppParser)
    def post(self):
        args = ppParser.parse_args()
        return updateRating(args)
    
    @require_token
    @require_admin
    @api.expect(ppParser)
    def put(self):
        args = ppParser.parse_args()
        return addRating(args)
    
    @require_token
    @require_admin
    @api.expect(getParser)
    def delete(self):
        args = getParser.parse_args()
        return deleteRating(args)