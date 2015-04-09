from BaseHTTPServer import BaseHTTPRequestHandler
import subprocess
import cgi
import os

class PostHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST'})
		songKeywords =  form.getvalue("keywords")
                print songKeywords
		subprocess.call(["youtube-dl", "--extract-audio",  "--default-search", "auto", str(songKeywords)])
if __name__ == '__main__':
	from BaseHTTPServer import HTTPServer
	server = HTTPServer(('206.87.194.102', 8080), PostHandler)
	print 'starting server'
	server.serve_forever()
       

