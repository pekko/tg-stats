#!/usr/bin/env python3
# coding: utf-8

import json
from flask import Flask

import analyze
import markov
import extra

msgs = analyze.get_msgs('output')
tg_markov = markov.TgMarkov(msgs)

app = Flask(__name__)

@app.route("/")
def main():
    return open('html/markov.htm').read()

@app.route("/<seed>")
def json_messages(seed):
    return json_messages_user(seed, None)

@app.route("/<seed>/<user>")
def json_messages_user(seed, user):
    msgs = tg_markov.run(10, user)
    altered_names = {}
    out = []
    for (name, msg) in msgs:
        if name not in altered_names:
            altered_names[name] = extra.alter_little(name, seed=seed).title()
        out.append((altered_names[name], msg))

    return json.dumps(out, ensure_ascii=False)

if __name__ == '__main__':
    app.run()
