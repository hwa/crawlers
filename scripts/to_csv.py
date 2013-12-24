#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import sys
from os.path import join as pjoin
import sqlite3

def flatten(list_list):
    return reduce(lambda x,y: x+y,
                  list_list,
                  [])

def unique(lst):
    return reduce(lambda z,i: z if i in z else z+[i],
                  lst,
                  [])

def split(reposts):
    relation = dict([(k, [d['repost-url'] for d in v]) for k,v in reposts.iteritems() if len(v) > 0])
    contents = [v for v in reposts.itervalues() if len(v) > 0]
    contents = unique(flatten(contents))
    return relation, contents


def read_json(json_file):
    with open(json_file, 'r') as jf:
        reposts = json.load(jf)
        relation, contents = split(reposts)
    return relation, contents

def write_csv(json_file, csv_dir):
    relation_csv_file = pjoin(csv_dir, 'relation.csv')
    contents_csv_file = pjoin(csv_dir, 'contents.csv')

    relation, contents = read_json(json_file)

    with open(relation_csv_file, 'w') as rcf:
        rcf.write('"from";"to"\n')
        for k,v in relation.iteritems():
            rcf.write(('%s;%s\n' % (k,v)))

    with open(contents_csv_file, 'w') as ccf:
        ccf.write('message;repost_num;repost_url;timestamp;username\n')
        for c in contents:
            ccf.wrqite(('%s;%s;%s;%s;%s\n'
                       % (c['msg'].replace(';','\\;'),
                          c['repost-num'],
                          c['repost-url'],
                          c['timestamp'],
                          c['username'].replace(';','\\;'))).encode('gbk',errors='ignore'))


def write_sqlite(json_file, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS relation')
    cur.execute('DROP TABLE IF EXISTS contents')
    cur.execute('CREATE TABLE relation (start TEXT, end TEXT)')
    cur.execute('CREATE TABLE contents (msg TEXT, repost_num INT, repost_url TEXT, timestamp INT, username TEXT)')

    relation, contents = read_json(json_file)

    for start, ends in relation.iteritems():
        relation[start] = unique(ends)

    for start, ends in relation.iteritems():
        for end in ends:
            sql = "INSERT INTO relation (start, end) VALUES ('%s', '%s')" % (start, end)
            cur.execute(sql)

    for c in contents:
        sql = ("INSERT INTO contents (msg, repost_num, repost_url, timestamp, username) VALUES ('%s', %s, '%s', %s, '%s')" % (c['msg'].replace("'", "''"), c['repost-num'], c['repost-url'], c['timestamp'], c['username'].replace("'","''"))).encode('utf-8')
        cur.execute(sql)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    json_file = sys.argv[1]
    csv_dir = sys.argv[2]
    sqlite_db = sys.argv[2]

    #write_csv(json_file, csv_dir)

    write_sqlite(json_file, sqlite_db)
