#!/usr/bin/env python3
# coding: utf-8

import itertools
import re

msgrow = re.compile("\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minutes>\d+)\]  (.*?) (?P<name>.*) (»»»|>>>) (?P<msg>.*)")
colors = re.compile("\x1b\[\d+(;\d+)?m")
emoji = re.compile('[^\u0000-\uD7FF\uE000-\uFFFF]')


def strip_colors(s):
    return colors.sub('', s)

def strip_emoji(s):
    return emoji.sub('', s)

def parse_row(row):
    plain = strip_colors(row.rstrip())
    match = msgrow.match(plain)
    if match == None:
        return None
    return match.groupdict()

def get_msgs(logfile):
    f = open(logfile)
    return [x for x in map(parse_row, f) if x != None]

def count_group(data, keyfunc, filterfunc=None):
    if filterfunc:
        data = filter(filterfunc, data)

    data = sorted(data, key=keyfunc)
    counts = [(k, len(list(g))) for (k,g) in itertools.groupby(data, keyfunc)]
    return counts

def average(data, groupfunc, countfunc):
    data = sorted(data, key=groupfunc)
    counts = []
    for (k,g) in itertools.groupby(data, groupfunc):
        numbers = list(map(countfunc, list(g)))
        avg = sum(numbers) / len(numbers)
        counts.append((k, avg))

    return counts

def percentage(data, keyfunc, filterfunc):
    total = dict(count_group(data, keyfunc))
    filtered = count_group(data, keyfunc, filterfunc)

    perc = [(key, filtered_count / total[key], filtered_count, total[key]) for (key, filtered_count) in filtered]
    return perc

def _print_table_generic(title, data, formatfunc):
    print()
    print(title.upper())
    print("="*len(title))
    for r in data:
        print(formatfunc(r))

def print_table(title, data, limit=None, desc=True):
    if limit == None:
        limit = len(data)
    data = sorted(data, key=lambda x:x[1], reverse=desc)
    _print_table_generic(title, data[:limit], lambda x: "%d\t%s" % (x[1], x[0]))

def print_table_perc(title, data, limit=None):
    if limit == None:
        limit = len(data)
    data = sorted(data, key=lambda x:x[1], reverse=True)
    _print_table_generic(title, data[:limit], lambda x: "%.0f %% (%d/%d)\t%s" % (x[1]*100, x[2], x[3], x[0]))

def main():
    def name(x): return x['name']

    msgs = get_msgs('output')

    count_by_name = count_group(msgs, name)
    print_table('Total', count_by_name, 20)

    threshold = 5
    count_dict = dict(count_by_name)
    threshold_msgs = [x for x in msgs if count_dict[x['name']] > threshold]
    msgs = threshold_msgs

    happy_smiley = percentage(msgs, name, lambda x: ':)' in x['msg'])
    print_table_perc('Happy people', happy_smiley, 3)

    sad_smiley = percentage(msgs, name, lambda x: ':(' in x['msg'])
    print_table_perc('Sad people', sad_smiley, 3)

    questions = percentage(msgs, name, lambda x: x['msg'].endswith('?'))
    print_table_perc('Asking questions', questions, 3)

    def has_cursing(x):
        cursewords = ['vittu', 'vitu', 'saatana', 'helvet', 'perkele', 'paska', 'jumalaut']
        words = x['msg'].lower().split()
        return any((w.startswith(c) for c in cursewords for w in words))

    cursing = percentage(msgs, name, has_cursing)
    print_table_perc('Cursing', cursing)

    night = count_group(msgs, name, lambda x: 0 <= int(x['hour']) <= 5)
    print_table('Night', night, 10)

    def is_shout(x):
        if x['msg'].endswith('!'):
            return True
        if len(x['msg']) > 3:
            return strip_emoji(x['msg']).upper() == x['msg']
        return False

    shout = count_group(msgs, name, is_shout)
    print_table('Shouters', shout, 5)

    lengths = average(msgs, name, lambda x: len(x['msg']))
    print_table('Longest messages', lengths, 10)
    print_table('Shortest messages', lengths, 10, desc=False)


if __name__ == '__main__':
    main()