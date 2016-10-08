#!../bin/python
import logging
from flask import session, Blueprint, request, render_template
from .helpers import registerUser, loginUser
from app.admin import admin

logger = logging.getLogger(__name__)
    
@admin.route('/login/', strict_slashes=False)
def login():
    ''' Login page '''
    return render_template("login.html")

@admin.route('/auth/login')
def authLogin():
    token = request.args.get('token', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return loginUser(token, provider)

@admin.route('/register/', strict_slashes=False)
def register():
    '''Register page'''
    return render_template("register.html")

@admin.route('/auth/register')
def authRegister():
    token = request.args.get('token', None, type=str)
    email = request.args.get('email', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return registerUser(token, email, provider)
    