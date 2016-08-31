#!/home/teamgoge/public_html/whiskey/main/bin/python
import ConfigParser
from utils import loginit
from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/login/', strict_slashes=False)
def login():
    return render_template("login.html")

@app.route('/')
@app.route('/frontend/', strict_slashes=False)
def frontend():
    return render_template("frontend.html")

@app.route('/minor/', strict_slashes=False)
def minor():
    return render_template("minor.html")

# TODO - disable caching for development.  Change to real caching for production
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#@app.route('/authorize/<provider>')
#def oauth_authorize(provider):
#    oauth = Social.get_provider(provider)
#    return oauth.authorize()

#@app.route('/callback/<provider>')
#def oauth_callback(provider):
#    oauth = Social.get_provider(provider)
#    socialId, email, firstName, lastName = oauth.callback()
#    if email is None:
#        return None
#    user = dbm.getUserByEmail(email)
    #if not user:
    #    dbm.addNormalUser(email=testEmail, facebookId=socialId, firstName=firstName, lastName=lastName)
    #    user = dbm.getUserByEmail(email)
        
#    return user

@app.errorhandler(404)
def not_found(error):
    return render_template('common/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('common/500.html'), 500

if __name__ == '__main__':
    loginit.initLogging()
    app.run(debug=False)
