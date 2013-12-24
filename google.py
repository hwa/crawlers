#-*- coding: utf-8 -*-

import datetime
import connect
from generic_crawler import crawl_search_engine
from utils import *

#
# connection
#
def is_forbidden(dom):
    if dom.find('input', id='captcha'):
        return True
    else:
        #raise Exception, 'got captcha'
        return False

def rq_dom(url):
    return connect.rq_dom(url, check_forbid=is_forbidden)

#
# exaction
#
def get_pagers(dom):
    nav = dom.find('table', id='nav')
    if nav:
        return (nav.find('a', id='pnprev'),
                nav.find('a', id='pnnext'))
    else:
        return (None, None)

def has_prev_page(dom):
    return True if get_pagers(dom)[0] else False

def has_next_page(dom):
    return True if get_pagers(dom)[1] else False

def extract_entries(dom):
    def _f(td):
        title = td.find('h3',class_='r').text
        url = td.find('h3',class_='r').find('a')['href']
        try:
            pub_date_ = td.find('span',class_='st').find('span', class_='f')
            pub_date = pub_date_.text.replace(' - ', '')
        except:
            pub_date = ''
        summary = td.find('span', class_='st')
        return {'title': title,
                'url': url,
                'pub_date': pub_date,
                'summary': summary}
    return map(_f, dom.find_all('li', class_='g'))

def search_sparse(mk_url, begin_date, end_date, word, quote_key=True, name='',
                  extract_entries=extract_entries):
    "搜索两个日期之间的关键词"
    def _mk_url(page):
        return mk_url(word, begin_date, end_date, page)
    def _before_start():
        print 'Getting %s on %s from %s to %s.' % (name, word, begin_date, end_date)
    def _uniquify(entries):
        return unique(entries, lambda e: e['title'])
    def _after_end(entries):
        print 'got %d %s entries.' % (len(entries), name)
    sleep_interval = 2 # sleep before getting next page
    return crawl_search_engine(_mk_url,
                               _before_start,
                               rq_dom,
                               extract_entries,
                               has_next_page,
                               sleep_interval,
                               _uniquify,
                               _after_end)
def search_dense(mk_url, begin_date, end_date, word,
                 quote_key=True, density=15, name='',
                 extract_entries=extract_entries):
    "搜索两个日期之间，以一段时间为精度的逐一搜索"
    dates = cut_dates(begin_date, end_date, density)
    ranges = zip(dates, dates[1:])
    entries = []
    for (d1,d2) in ranges:
        entries += search_sparse(mk_url, d1,d2, word, quote_key, name, extract_entries)
    return entries

#
# persistence
#
def write_sqlite(news, db):
    news_ = []
    for company, entries in news:
        for entry in entries:
            entry['company'] = company
            news_.append(entry)
    fields = [('company','TEXT'),
              ('pub_date', 'TEXT'),
              ('source', 'TEXT'),
              ('summary', 'TEXT'),
              ('title', 'TEXT'),
              ('url', 'TEXT')]
    persist.save_dicts(news_, db, "news", fields)


def write_sqlite_eventname(news, db):
    """
    """
    for entry in news:
        entry['keyword'] = entry['keyword'].strip()
        entry['number'] = entry['No.']
    fiedls = [('number','INT'),
              ('keyword', 'TEXT'),
              ('pub_date', 'TEXT'),
              ('source', 'TEXT'),
              ('summary', 'TEXT'),
              ('title', 'TEXT'),
              ('url', 'TEXT')]
    persist.save_dicts(news, db, "news", fields)
