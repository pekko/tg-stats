#!/usr/bin/env python3.3
# coding: utf-8

import json
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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        user = urllib.parse.unquote(self.path[1:])
        if user == '':
            user = None

        p(json.dumps(list(tg_markov.run(10, user))))

def main(port):
    global tg_markov

    msgs = analyze.get_msgs('output')
    tg_markov = markov.TgMarkov(msgs)

    httpd = http.server.HTTPServer(('', port), MarkovHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print("Usage: %s port")
        sys.exit()
    main(int(sys.argv[1]))