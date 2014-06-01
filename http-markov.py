#!/usr/bin/env python3.3
# coding: utf-8

import json
import http.server
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