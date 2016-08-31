#!/home/teamgoge/public_html/whiskey/main/bin/python

from flup.server.fcgi import WSGIServer
def app(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	return('''Hello world!\\n''')
WSGIServer(app).run()
