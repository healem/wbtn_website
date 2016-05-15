#!../bin/python
from flup.server.fcgi import WSGIServer
import rest_server

if __name__ == '__main__':
    WSGIServer(rest_server).run()
