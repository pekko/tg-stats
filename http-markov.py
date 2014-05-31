#!/usr/bin/env python3.3
# coding: utf-8

import http.server
import urllib.parse

import analyze
import markov

tg_markov = None

class MarkovHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		def p(s):
			self.wfile.write(s.encode('utf-8'))
		self.send_response(200)
		self.end_headers()

		user = urllib.parse.unquote(self.path[1:])
		p(user+"\n")
		p(tg_markov.run(10, user))

def main():
	global tg_markov

	msgs = analyze.get_msgs('output')
	tg_markov = markov.TgMarkov(msgs)

	httpd = http.server.HTTPServer(('localhost', 1337), MarkovHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		httpd.server_close()


if __name__ == '__main__':
	main()