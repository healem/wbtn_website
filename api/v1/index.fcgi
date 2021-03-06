#!/home/bythenum/public_html/whiskey/api/bin/python
from flup.server.fcgi import WSGIServer
from rest_server import app
import sys

sys.path.append("/home/bythenum/public_html/whiskey/api/v1")

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
