#!/usr/bin/env python3.3
# coding: utf-8

import json
import http.server
import os
import urllib.parse

import analyze
import markov
import extra

tg_markov = None

class MarkovHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        def p(s):
            self.wfile.write(s.encode('utf-8'))
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        (seed,user) = [urllib.parse.unquote(x) for x in self.path[1:].split("/")]
        if user == '':
            user = None

        msgs = tg_markov.run(10, user)
        altered_names = {}
        out = []
        for (name, msg) in msgs:
            if name not in altered_names:
                altered_names[name] = extra.alter_little(name, seed=seed).title()
            out.append((altered_names[name], msg))

        p(json.dumps(out, ensure_ascii=False))

    def log_message(self, format, *args):
        f = open('http-markov.log', 'a')
        f.write(self.log_date_time_string()+" ")
        f.write(format % args)
        f.write("\n")
        f.close()

def main(port):
    global tg_markov

    msgs = analyze.get_msgs('output')
    tg_markov = markov.TgMarkov(msgs)

    httpd = http.server.HTTPServer(('', port), MarkovHandler)
    pid = os.fork()
    if pid == 0:
        pidfile = open('http-markov.pid', 'w')
        pidfile.write(str(os.getpid()))
        pidfile.close()
        httpd.serve_forever()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print("Usage: %s port")
        sys.exit()
    main(int(sys.argv[1]))