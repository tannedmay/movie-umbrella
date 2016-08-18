import logging

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
import routes

from utils import configure_logging
import db
configure_logging()

# class HTTPRequestHandler(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#         self.wfile.write()
#
#     def do_POST(self):
#         self._set_headers()
#         print "in post method"
#         self.data_string = self.rfile.read(int(self.headers['Content-Length']))
#
#         self.send_response(200)
#         self.end_headers()
#
#         data = simplejson.loads(self.data_string)
#         with open("test123456.json", "w") as outfile:
#             simplejson.dump(data, outfile)
#         print "{}".format(data)
#         f = open("for_presen.py")
#         self.wfile.write(f.read())
#         return


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=80):
    # Setup a route mapper
    mapper = routes.Mapper()
    mapper.connect("movie_search", "/movie",
                   controller='db',
                   action="search",
                   conditions=dict(method=["GET"]))
    mapper.connect("movie_get", "/movie/{_id}",
                   controller='db',
                   action="get",
                   conditions=dict(method=["GET"]))
    mapper.connect("movie_create", "/movie",
                   controller='db',
                   action="create",
                   conditions=dict(method=["POST"]))
    mapper.connect("movie_update", "/movie/{_id}",
                   controller='db',
                   action="update",
                   conditions=dict(method=["PUT"]))
    mapper.connect("movie_delete", "/movie/{_id}",
                   controller='db',
                   action="delete",
                   conditions=dict(method=["DELETE"]))

    mapper.controller_scan("./")

    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd server at port: %d" % port)
    httpd.serve_forever()

if __name__ == "__main__":
    run(port=8000)
