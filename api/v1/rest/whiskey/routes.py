#!../../../bin/python
import logging
import json
from flask import session
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from flask_restplus.inputs import boolean
from db import datastore
from ..restplus import api
from ..decorators import require_token, require_admin
from helpers import addWhiskey, deleteWhiskey, updateWhiskey

logger = logging.getLogger("whiskey-routes")
whiskeyApi = Namespace('whiskey', description='Whiskey related operations')

whiskey = whiskeyApi.model('Whiskey', {
    'name': fields.String(required=True, description='The name of the whiskey'),
    'proof': fields.Float(required=True, description='The proof of the whiskey'),
    'price': fields.Float(required=True, description='The price of the whiskey'),
    'style': fields.String(required=True, description='The style of whiskey'),
    'age': fields.Integer(required=True, description='The age of the whiskey'),
    'icon': fields.Url(required=False, absolute=True, description='The url for the whiskey icon'),
    'url': fields.Url(required=False, absolute=True, description='The original url for the whiskey icon')
})

dbm = datastore.DbManager(testMode=False)

getAllParser = whiskeyApi.parser()
getAllParser.add_argument('currentPage', type=int, required=True, default=1, help='Current page of the query, count starts at 1')
getAllParser.add_argument('itemsPerPage', type=int, required=True, default=20, help='Number of items returned per page, max=100')
getAllParser.add_argument('sortField', type=str, required=True, default='name', help='The name of the field to sort on: name, price, proof, style, or age')

getParser = whiskeyApi.parser()
getParser.add_argument('name', type=str, required=True, help='The name of the whiskey')

postParser = whiskeyApi.parser()
postParser.add_argument('name', type=str, required=True, help='The name of the whiskey')
postParser.add_argument('proof', type=float, required=False, help='The proof of the whiskey')
postParser.add_argument('price', type=float, required=False, help='The price of the whiskey')
postParser.add_argument('style', type=str, required=False, help='The style of the whiskey')
postParser.add_argument('age', type=int, required=False, help='The age of the whiskey')
postParser.add_argument('icon', type=str, required=False, help='The url for the whiskey icon')
postParser.add_argument('url', type=str, required=False, help='The original url for the whiskey icon')

putParser = whiskeyApi.parser()
putParser.add_argument('name', type=str, required=True, help='The name of the whiskey')
putParser.add_argument('proof', type=float, required=True, help='The proof of the whiskey')
putParser.add_argument('price', type=float, required=True, help='The price of the whiskey')
putParser.add_argument('style', type=str, required=True, help='The style of the whiskey')
putParser.add_argument('age', type=int, required=True, help='The age of the whiskey')
putParser.add_argument('icon', type=str, required=False, default=None, help='The url for the whiskey icon')
putParser.add_argument('url', type=str, required=False, default=None, help='The original url for the whiskey icon')

@api.route('/allwhiskies')
class WBTNWhiskies(Resource):
    @require_token
    @api.expect(getAllParser, True)
    def get(self):
        #logger.debug("Incoming request for all whiskies")
        args = getAllParser.parse_args()
        #logger.debug("Getting all whiskies with args: %s", args)
        allWhiskies = dbm.getAllWhiskies(args['currentPage'], args['itemsPerPage'], args['sortField'])
        #logger.debug("Returning allWhiskies: %s", allWhiskies)
        return allWhiskies
    
@api.route('/whiskey')
class WBTNWhiskey(Resource):
    @require_token
    @api.expect(getParser)
    def get(self):
        args = getParser.parse_args()
        return json.dumps(getWhiskeyByName(args['name']).__dict__)
    
    @require_token
    @require_admin
    @api.expect(postParser)
    def post(self):
        args = postParser.parse_args()
        return updateWhiskey(args)
    
    @require_token
    @require_admin
    @api.expect(putParser)
    def put(self):
        args = putParser.parse_args()
        return addWhiskey(args)
    
    @require_token
    @require_admin
    @api.expect(getParser)
    def delete(self):
        args = getParser.parse_args()
        return deleteWhiskey(args)
    
def getWhiskeyByName(name):
    return dbm.getWhiskeyByName(name)