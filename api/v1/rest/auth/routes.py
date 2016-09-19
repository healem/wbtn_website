#!../../bin/python
import logging
from flask import session, Blueprint
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from ..restplus import api
from .helpers import registerUser, loginUser

logger = logging.getLogger(__name__)
authApi = Namespace('auth', description='User authentication and authorization related operations')

authRegister = authApi.model('Register', {
    'token': fields.String(required=True, description='The user access token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
    'email': fields.String(required=True, description='Email address of the user'),
})

authLogin = authApi.model('Login', {
    'token': fields.String(required=True, description='The user access token'),
    'provider': fields.Integer(required=True, description='The provider the token belongs to'),
})

regParser = authApi.parser()
regParser.add_argument('token', type=str, required=True, help='The user access token')
regParser.add_argument('provider', type=int, required=True, help='The provider the token belongs to')
regParser.add_argument('email', type=str, required=True, help='Email address of the user')

loginParser = authApi.parser()
loginParser.add_argument('token', type=str, required=True, help='The user access token')
loginParser.add_argument('provider', type=int, required=True, help='The provider the token belongs to')

@api.route('/register')
@api.expect(regParser)
class AuthRegister(Resource):
    @api.marshal_list_with(authRegister)
    def post(self):
        args = regParser.parse_args()
        return registerUser(args['token'], args['provider'], args['email'])
    
@api.route('/login')
@api.expect(loginParser)
class AuthLogin(Resource):
    @api.marshal_list_with(authLogin)
    def post(self):
        args = loginParser.parse_args()
        return loginUser(args['token'], args['provider'])
    