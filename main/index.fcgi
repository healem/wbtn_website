#!/home/teamgoge/public_html/whiskey/main/bin/python
import sys
import os
#sys.path.insert(0, '/home/teamgoge/public_html/whiskey/main/lib/python2.7/site-packages')
from flup.server.fcgi import WSGIServer
from frontend import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
