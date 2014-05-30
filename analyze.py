#!/usr/bin/env python3.3
# coding: utf-8

from collections import defaultdict
import itertools
import re

msgrow = re.compile("\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minutes>\d+)\]  NappiGram (?P<name>.*) (»»»|>>>) (?P<msg>.*)")
colors = re.compile("\x1b\[\d+(;\d+)?m")

def strip_colors(s):
    return colors.sub('', s)

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
    groups = []
    counts = [(k, len(list(g))) for (k,g) in itertools.groupby(data, keyfunc)]
    return sorted(counts, key=lambda x:x[1], reverse=True)

def percentage(data, keyfunc, filterfunc):
    total = dict(count_group(data, keyfunc))
    filtered = count_group(data, keyfunc, filterfunc)

    perc = [(key, filtered_count / total[key]) for (key, filtered_count) in filtered]
    return perc

def main():
    def name(x): return x['name']

    msgs = get_msgs('output')
    count_by_name = count_group(msgs, name)
    print(percentage(msgs, name, lambda x: ':)' in x['msg']))





if __name__ == '__main__':
    main()