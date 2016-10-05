#!/home/bythenum/public_html/whiskey/main/bin/python
from os import path, walk
import ConfigParser
import logging
from utils import loginit
from flask import Flask, jsonify, render_template, request
from auth import registerUser, loginUser

loginit.initLogging()
app = Flask(__name__)
app.logger.setLevel("DEBUG")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/login/', strict_slashes=False)
def login():
    ''' Login page '''
    return render_template("login.html")

@app_route('/auth/login')
def authLogin():
    token = request.args.get('token', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return loginUser(token, provider)

@app.route('/register/', strict_slashes=False)
def register():
    '''Register page'''
    return render_template("register.html")

@app_route('/auth/register')
def authRegister():
    token = request.args.get('token', None, type=str)
    email = request.args.get('email', None, type=str)
    provider = request.args.get('provider', 1, type=int)
    return registerUser(token, email, provider)

@app.route('/')
def frontend():
    ''' Front landing page '''
    return render_template("frontend.html")

@app.route('/minor/')
def minor():
    ''' Minor '''
    return render_template("minor.html")

#@app.route('/main/help', methods = ['GET'])
def print_help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

# TODO - disable caching for development.  Change to real caching for production
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

extra_dirs = ['templates',
              'templates/common',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

@app.errorhandler(404)
def not_found(error):
    app.logger.error('Page not found: %s', request.path)
    return render_template('common/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Internal error: %s at path: %s', error, request.path)
    return render_template('common/500.html'), 500

if __name__ == '__main__':
    app.run(debug=False, extra_files=extra_files)
