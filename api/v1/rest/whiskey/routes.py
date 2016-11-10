#!../../../bin/python
import logging
import json
from flask import session
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from flask_restplus.inputs import boolean
from db import datastore
from ..restplus import api
from ..decorators import require_token, require_admin

logger = logging.getLogger("whiskey-routes")
whiskeyApi = Namespace('whiskey', description='Whiskey related operations')

whiskey = whiskeyApi.model('Whiskey', {
    'name': fields.String(required=True, description='The name of the whiskey'),
    'proof': fields.Float(required=True, description='The proof of the whiskey'),
    'price': fields.Float(required=True, description='The price of the whiskey'),
    'style': fields.String(required=True, description='The style of whiskey'),
    'age': fields.Integer(required=True, description='The age of the whiskey'),
    'icon': fields.Url(required=True, absolute=True, description='The url for the whiskey icon'),
})

dbm = datastore.DbManager(testMode=False)

getAllParser = whiskeyApi.parser()
getAllParser.add_argument('currentPage', type=int, required=True, default=1, help='Current page of the query, count starts at 1')
getAllParser.add_argument('itemsPerPage', type=int, required=True, default=20, help='Number of items returned per page, max=100')
getAllParser.add_argument('sortField', type=str, required=True, default='name', help='The name of the field to sort on: name, price, proof, style, or age')

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