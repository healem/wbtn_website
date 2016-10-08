#!../bin/python
import logging
from flask import session, Blueprint, request, render_template
from .helpers import registerUser, loginUser

logger = logging.getLogger(__name__)
auth = Blueprint('auth', __name__)
    
@auth.route('/login/', strict_slashes=False)
def login():
    ''' Login page '''
    return render_template("login.html")

@auth.route('/auth/login')
def authLogin():
    token = request.args.get('token', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return loginUser(token, provider)

@auth.route('/register/', strict_slashes=False)
def register():
    '''Register page'''
    return render_template("register.html")

@auth.route('/auth/register')
def authRegister():
    token = request.args.get('token', None, type=str)
    email = request.args.get('email', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return registerUser(token, email, provider)
    