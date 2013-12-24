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
# extraction
#

def get_pagers():
    pager = dom.find('p', id='page')
    if pager:
        pn = pager.find_all('a', class_='n')
        if len(pn) == 2:
            return tuple(pn)
        elif len(pn) == 1 and u'上一页' in pn[0].text:
            return (pn[0], None)
        elif len(pn) == 1:
            return (None, pn[0])
    else:
        return (None, None)

def has_prev_page(dom):
    return True if get_pagers(dom)[0] else False

def has_next_page(dom):
    return True if get_pagers(dom)[1] else False



def mk_url(begin_time, end_time, word, entry_begin):
    word_quote = urllib.quote(word)
    # 每页100条
    return 'http://news.baidu.com/ns?bt=%s&et=%s&si=&rn=100&tn=newsdy&ie=utf8&ct=0&word=%s&pn=%d&cl=2' % (begin_time, end_time, word_quote, entry_begin)

def extract_entries(dom):
    def _f(li):
        ttl = li.find('h3', class_='c-title').find('a')
        title, url = ttl.text, ttl['href']
        src = li.find('span', class_='c-author').text.replace(u'\xa0',' ')
        #source, pub_date, pub_time = src.split(' ')
        src_ptn = r'(.*) (\d\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d)'
        source,pub_date, pub_time = re.search(src_ptn, src).groups()
        summary = li.find('div', class_='c-summary').text
        return {'title': title,
                'url': url,
                'source': source,
                'pub_date': pub_date,
                'pub_time': pub_time,
                'summary': summary}
    es = map(_f, dom.find('ul').find_all('li', class_='result'))
    print '\tgot %d news' % len(es)
    return es



def get_news(begin_date, end_date, word, quote_key=True):
    print 'Getting news on %s from %s to %s.' % (word, begin_date, end_date)
    word = '"%s"' % word if quote_key else '%s' % word
    begin_time, end_time = ("", "")
    begin_time = "" if not begin_date else datetime.datetime.strptime('%s 00:00:00' % begin_date,
                                                                      '%Y-%m-%d %H:%M:%S').strftime('%s')
    end_time = "" if not end_date else datetime.datetime.strptime('%s 23:59:59' % end_date,
                                                                  '%Y-%m-%d %H:%M:%S').strftime('%s')
    total, entries = get_first_page(mk_url(begin_time, end_time, word, 0))
    for p in range(1, int(ceil(total/100.0))):
        print 'Getting page %d' % (p+1)
        url = mk_url(begin_time, end_time, word, p*100)
        #r = requests.get(url)
        #dom = bs4.BeautifulSoup(r.content.decode('gbk',errors='ignore'))
        r, dom = rq_dom(url)
        try:
            entries += extract_entries(dom)
        except:
            break
        pagers = dom.find('p', id='page').find_all('a',class_='n')
        if len(pagers) == 0:
            break
        if len(pagers) == 1 and pagers[-1].text == u'<\u4e0a\u4e00\u9875':
            break

    return total, unique(entries, lambda e: e['title'])


def unique(seq, get_key):
    return reduce(lambda (k,z),i: (k,z) if get_key(i) in k else (k+[get_key(i)], z+[i]),
                  seq,
                  ([],[]))[1]

def get_news_dates(data_file):
    def _f(d):
        d2 = datetime.datetime.strptime(d, '%Y.%m')
        d0 = (d2 - datetime.timedelta(182)).strftime('%Y-%m-%d')
        d1 = (d2 + datetime.timedelta(213)).strftime('%Y-%m-%d')
        return [d0, d1]

    with open(data_file, 'r') as df:
        return [_f(d) + [n] for d, n in  [i.strip().split('\t') for i in df.readlines()]]


def months_delta(year, month, delta):
    a = year*12 + month - 1 + delta
    y = a/12
    m = a % 12
    return (y, m+1)

###
def half_year_around(year, month):
    ds1 = [months_delta(year, month, i) for i in range(-6, 7)]
    ds2 = [months_delta(year, month, i) for i in range(-5, 8)]
    ds = zip(ds1, ds2)
    return [(datetime.datetime(*d[0], day=1).strftime('%Y-%m-%d'),
             datetime.datetime(*d[1], day=1).strftime('%Y-%m-%d'))
            for d in ds]

###
def get_news_dates2(data_file):
    with open(data_file, 'r') as df:
        return [[half_year_around(*map(int, d.split('.'))), n]
                for d, n in [i.strip().split('\t') for i in df.readlines()]]

###
def get_news2(dates, word):
    news = [0,[]]
    for (begin_date, end_date) in dates:
        #time.sleep(2)
        d = get_news(begin_date, end_date, word)
        news[0] += d[0]
        news[1] += d[1]
    return news



def write_sqlite(news, db):
    """
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS news')
    cur.execute('CREATE TABLE news (company TEXT, pub_date TEXT, pub_time TEXT, source TEXT, summary TEXT, title TEXT, url TEXT)')

    for company, entries in news.iteritems():
        #company = company.decode('utf-8')
        for entry in entries:
            v = (company, entry['pub_date'], entry['pub_time'], entry['source'], entry['summary'], entry['title'], entry['url'])
            sql = "INSERT INTO news (company, pub_date, pub_time, source, summary, title, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % v
            sql = sql.encode('utf-8')
            cur.execute(sql)

    conn.commit()
    conn.close()




##
def get_all_news(word, y0, m0, dd0, y1, m1, dd1):
    print 'Getting news on %s' % word
    news = [0, []]
    d0 = datetime.datetime(y0, m0, dd0)
    d1 = datetime.datetime(y1, m1, dd1)
    for dd in range(1,(d1-d0).days/30):
        d1 = (d0 + datetime.timedelta(30))
        d1_ = d1.strftime('%Y-%m-%d')
        d0_ = d0.strftime('%Y-%m-%d')
        n = get_news(d0_, d1_, word)
        news[0] += n[0]
        news[1] += n[1]
        d0 = d1

    return news


##
def write_sqlite_eventname(news, db):
    """
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS news')
    cur.execute('CREATE TABLE news (number INT, keyword TEXT, pub_date TEXT, pub_time TEXT, source TEXT, summary TEXT, title TEXT, url TEXT)')

    for n in news:
        #company = company.decode('utf-8')
        keyword = n['keyword'].strip()
        num = n['No.']
        entries = n['news'][1]
        for entry in entries:
            v = (num, keyword, entry['pub_date'], entry['pub_time'], entry['source'], entry['summary'], entry['title'], entry['url'])
            v = tuple([i.replace("'", "''") if type(i) == unicode else i for i in v])
            sql = u"INSERT INTO news (number, keyword, pub_date, pub_time, source, summary, title, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % v
            sql = sql.encode('utf-8')
            print sql
            cur.execute(sql)


    conn.commit()
    conn.close()
