#-*- coding: utf-8 -*-

import datetime
import google_blog as gb


def read_company_birthes(file_name):
    "read companies' birthes from file"
    lines = open(file_name).readlines()
    bs = [l.strip().split('\t') for l in lines]
    bs = [(datetime.datetime.strptime(b,'%Y.%m'), c) for [b,c] in bs]
    return bs

def google_blogs_about_companies():
    "crawl google blogs about companies "
    birthes = read_company_birthes('data/news/company_birth.txt')
    entries = []
    for (b, c) in birthes:
        print 'getting google blogs about %s' % c
        now = datetime.datetime.now()
        entries += gb.get_blogs_dense(b, now, c+' 公司')
    print 'writing into sqlite db.'
    gb.write_sqlite(entries, 'google_blog.db')
