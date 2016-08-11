#!../bin/python
import ConfigParser
import db.datastore
import utils.loginit
import social.interface
from db import datastore
from utils import loginit

from flask import Flask, jsonify

app = Flask(__name__)

loginit.initTestLogging()
dbm = datastore.DbManager(testMode=True)

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = Social.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = Social.get_provider(provider)
    socialId, email, firstName, lastName = oauth.callback()
    if email is None:
        return None
    user = dbm.getUserByEmail(email)
    if not user:
        dbm.addNormalUser(email=testEmail, facebookId=socialId, firstName=firstName, lastName=lastName)
        user = dbm.getUserByEmail(email)
        
    return user

if __name__ == '__main__':
    loginit.initLogging()
    app.run(debug=True)

