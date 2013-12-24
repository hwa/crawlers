#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import json
import urllib
import base64
import hashlib
import requests
import rsa
import binascii
import bs4
from datetime import datetime, time, date, timedelta
import sys
import pickle
import time as ttime
import envoy
import os
import to_csv
import pymongo
import time as ttime
import sqlite3

def tlog_(log_file, newline='\n', timestamp=True):
    def _f(msg):
        if timestamp:
            n = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            n = ''
        with open(log_file, 'ab') as logfile:
            logfile.write("%s %s%s" % (n, msg.encode('utf8'), newline))
    return _f

tlog = tlog_('crawler.log')
tlogs = tlog_('crawler.log', '')
tloga = tlog_('crawler.log', '\n', False)




WBCLIENT = 'ssologin.js(v.1.4.5)'
sha1 = lambda x: hashlib.sha1(x).hexdigest()


def wblogin(username, password):
    session = requests.session(
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHT'
                          'ML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
        }
    )
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sina'
        'SSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=%s' %
        (base64.b64encode(username), WBCLIENT)
    )
    pre_login_str = re.match(r'[^{]+({.+?})', resp.content).group(1)
    pre_login_json = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'useticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(urllib.quote(username)),
        'service': 'miniblog',
        'servertime': pre_login_json['servertime'],
        'nonce': pre_login_json['nonce'],
        'pcid': pre_login_json['pcid'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'rsakv': pre_login_json['rsakv'],
        'sp': get_pwd_rsa(password,
                          pre_login_json['servertime'],
                          pre_login_json['nonce']),
        'encoding': 'UTF-8',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META',
        'prelt': 476
    }
    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
    )
    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.content).group(1)
    resp = session.get(login_url)
    print resp.content
    #login_str = re.match(r'[^{]+({.+?}})', resp.content).group(1)
    login_str = re.match(r'[^{]+({.+})', resp.content).group(1)

    return json.loads(login_str), session


def get_pwd_rsa(pwd, servertime, nonce):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    #n, n parameter of RSA public key, which is published by WEIBO.COM
    #hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

    #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e = 65537

    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)

    #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)

    #get encrypted password
    encropy_pwd = rsa.encrypt(message, key)

    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encropy_pwd)

#login_str, session = wblogin('cheng.zhang@gmail.com','1qa2ws')
#'http://weibo.com/1156988152/eArF61HEkKf?type=repost'
def get_first_page_post(session, url):
    tlogs("[INFO] \tgetting reposts of first page ...")
    r = session.get(url)

    if r.url == 'http://weibo.com/sorry?pagenotfound':
        tloga('not found.')
        tlog('[WARN] \turl is not found: %s' % url)
        return 0, 0, [], ''

    dom = bs4.BeautifulSoup(r.content)

    scripts = [s.text for s in dom.find_all('script') if s.text.find('pl_content_weiboDetail') > -1]
    if len(scripts) > 0:
        script = scripts[0]
    else:
        tloga('error')
        tlog('[WARN] \turl error: %s, %s' % (r.url, r.text))
        return 0,0,[],''

    ct = json.loads(script[script.find('{"pid'):-1])

    rp_dom = bs4.BeautifulSoup(ct['html'])

    num = parse_num(rp_dom.find('a', attrs={'node-type': 'forward_counter'}).text)

    pages = rp_dom.find_all('a', attrs={'action-type':'feed_list_page'})
    if len(pages) > 0:
        page = int(pages[-1].text)
    else:
        page = 1

    url = paging_url(rp_dom) if page > 1 else None

    tloga("got.")
    return num, page, reposts(rp_dom), url

def get_repost_page(session, main_url, page):
    tlogs("[INFO] \tgetting reposts of page %d ... " % page)
    url = page_url(main_url, page)
    r = session.get(url)
    rp_dom = bs4.BeautifulSoup(json.loads(r.content)['data']['html'])
    tloga("got.")
    return reposts(rp_dom)

def page_url(main_url, page):
    return '%s&page=%d&__rnd=%s' % (main_url,
                                    page,
                                    datetime.now().strftime('%s'))

def paging_url(rp_dom):
    #ad = rp_dom.find('a', class_='btn_page_next').find('span')['action-data']
    ad = rp_dom.find('span', attrs={'action-type':'feed_list_page'})['action-data']
    id_ = re.search(r'id=(\d+)', ad).group(1)
    mid = re.search(r'max_id=(\d+)', ad).group(1)
    url = 'http://weibo.com/aj/mblog/info/big?_wv=5&id=%s&max_id=%s&_t=0'
    return url % (id_, mid)


def has_next_page(rp_dom):
    return True if rp_dom.find('a', class_='page') else False

def reposts(rp_dom):
    return map(repost, rp_dom.find_all('dl', class_='comment_list'))

def repost(rp_dl):
    dd = rp_dl.find('dd')
    a = dd.find('a', attrs={'action-type':'feed_list_forward'})
    u = dd.find('a', usercard=re.compile(r'.+'))
    return {"username": u.text,
            "userid": u['usercard'][3:],
            "msg": dd.find('em').text,
            "timestamp": parse_time(dd.find('span',recursive=False).text),
            "repost-num": parse_num(a.text),
            "repost-url": parse_url(a['action-data'])
            }

def parse_num(txt):
    r = re.compile(ur'\u8f6c\u53d1\((\d+)\)')
    rs = re.search(r, txt)
    if rs:
        return int(rs.group(1))
    else:
        return 0

def parse_url(href):
    r = re.compile(r'&url=([^&]+)&')
    return re.search(r, href).group(1)

def parse_time(time_str):
    try:
        t = datetime.strptime(time_str, '(%Y-%m-%d %H:%M)')
    except ValueError:
        seconds_ago = re.compile(ur'\((\d+)\u79d2\u524d\)')
        minutes_ago = re.compile(ur'\((\d+)\u5206\u949f\u524d\)')
        hour_min  = re.compile(ur'\(\u4eca\u5929 (\d+):(\d+)\)')
        date_hour_min = re.compile(ur'\((\d+)\u6708(\d+)\u65e5 (\d+):(\d+)\)')
        if re.search(hour_min, time_str):
            h, m = re.search(hour_min, time_str).groups()
            t = datetime.combine(datetime.today().date(),
                                    time(int(h), int(m)))
        elif re.search(minutes_ago, time_str):
            m = re.search(minutes_ago, time_str).group(1)
            t = (datetime.today() - timedelta(minutes=int(m)))
        elif re.search(seconds_ago, time_str):
            s = re.search(seconds_ago, time_str).group(1)
            t = (datetime.today() - timedelta(seconds=int(s)))
        elif re.search(date_hour_min, time_str):
            M,d,h,m =  map(int, re.search(date_hour_min, time_str).groups())
            this_year = datetime.today().year
            t = datetime(this_year, M, d, h, m)
        else:
            print time_str
            raise Exception("time format unknow: %s" % time_str.encode('utf-8'))
    return t.strftime('%s')



def recursively_crawl_reposts(session, seeds):
    T = 3
    def _f(url):
        tlog("[INFO] Crawling %s" % url)
        num, page, reposts, main_url = get_first_page_post(session, url)
        tlog( "[INFO] \thas %d reposts, and %d pages." % (num, page))
        for p in range(2, page+1):
            t0 = ttime.time()
            reposts += get_repost_page(session, main_url, p)
            dt = ttime.time() - t0
            if dt < T:
                ttime.sleep(T - dt)
        return (reposts,
                [i['repost-url'] for i in reposts if i['repost-num'] > 0])

    def paramize(url):
        return url.split('?')[0] + '?type=repost'

    def _g(reposts_tree, next_urls):
        if len(next_urls) > 0:
            tlog('[INFO] Crawling reposts of %d weibo.' % len(next_urls))
        else:
            tlog('[INFO] Crawling ends.')
        if len(next_urls) == 0:
            return reposts_tree
        nu = []
        for url in next_urls:
            if reposts_tree.has_key(url):
                tlog('[WARN]\t crawled: %s' % url)
                continue
            t0 = ttime.time()
            r, n = try_times(10,
                             lambda : _f(paramize(url)))
            reposts_tree[url] = r
            nu += n
            dt = ttime.time() - t0
            if dt < T:
                ttime.sleep(T - dt)
        nu = list(set(nu))
        return _g(reposts_tree, nu)

    return _g({}, seeds)

def try_times(times, func):
    n = 0
    while n < times:
        try:
            return func()
        except Exception as e:
            print e
            n += 1
            ttime.sleep(10)

def crawl_save(session, iname):
    ddir = os.path.join('data', iname)
    seeds_file = os.path.join('data', iname, 'seeds')
    with open(seeds_file, 'r') as sf:
        seeds = [s.strip().split('?')[0] for s in sf.readlines()] # 去掉链接参数

    reposts_tree = recursively_crawl_reposts(session, seeds)

    json_file = os.path.join('data', iname, iname+'.json')

    with open(json_file, 'w') as of:
        json.dump(reposts_tree, of)
        tlog('[INFO]\t dump to output file.')

    db_file = os.path.join('data', iname, iname + '.db')

    to_csv.write_sqlite(json_file, db_file)

    #envoy.run('cd %s; cat ../../dump_csv.sql|sqlite3 %s' % (ddir, iname+'.db'))



def crawl(iname):
    print 'Crawling %s' % iname
    #login_str, session = wblogin('strawberry_234@163.com', 'strawberry')
    login_str, session = wblogin('zc_cheng@21cn.com', '1qa2ws')

    crawl_save(session, iname)




def crawl_user_info(session, user_home_url):
    r = session.get(user_home_url, timeout=60)
    dom = bs4.BeautifulSoup(r.content)
    def _g(txt):
        scripts = [s.text for s in dom.find_all('script') if s.text.find(txt) > -1]
        if len(scripts) > 0:
            script = scripts[0]
        else:
            tloga('error')
            tloga('\turl: %s' % user_home_url)
            return

        html = json.loads(script[script.find('{"ns":"pl.header.head.index"'):-1])['html']
        u_dom = bs4.BeautifulSoup(html)
        return u_dom

    #u_dom = _g('pl_profile_photo')
    u_dom = _g('"ns":"pl.header.head.index"')
    if not u_dom:
        return
    try:
        guanzhu = int(u_dom.find('strong', attrs={'node-type':'follow'}).text)
        fensi = int(u_dom.find('strong', attrs={'node-type':'fans'}).text)
        weibo = int(u_dom.find('strong', attrs={'node-type':'weibo'}).text)
    except AttributeError:
        return


    #u_dom = _g('pl_profile_hisInfo')
    #if not u_dom:
    #    return
    name = u_dom.find('span', class_='name').text

    return name, guanzhu, fensi, weibo


conn = pymongo.Connection()
db = conn['zc']
coll = db['weibo_user_info']

def save(url, name, guanzhu, fensi, weibo):
    coll.insert({'_id': name,
                 'url': url,
                 'guanzhu': guanzhu,
                 'fensi': fensi,
                 'weibo': weibo})


def run_get_user(session, start=0):
    users = open('./data/weibo/weibo_users.u.txt','r').readlines()
    users = [i.strip() for i in users]
    for u in users[start:]:
        if coll.find({'url': u}).count() == 0:
            print u
            x = crawl_user_info(session, u)
            print x
            if x:
                save(u, *x)
            else:
                coll.insert({'url': u,
                             'got': None})
        else:
            print "already got %s" % u
            #     ttime.sleep(1)
            # except Exception as e:
            #     print 'get exception %s' % e
            #     print 'sleeping 1 hour'
            #     ttime.sleep(3600)
            #     save(u,*crawl_user_info(session, u))



def ipy_run():
    l,s = wblogin('zc_cheng@21cn.com', '1qa2ws')
    done = False
    while not done:
        try:
            run_get_user(s,coll.find().count())
            done = True
        except Exception as e:
            print e
            print 'sleeping 10 minutes'
            ttime.sleep(600)
            l,s = wblogin('zc_cheng@21cn.com', '1qa2ws')


def write_sql(db, users_info):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS weibo_users_info')
    cur.execute('CREATE TABLE weibo_users_info (name TEXT, fans INT, followings INT, url TEXT, posts INT )')

    for user in users_info:
        if not user.has_key('got'):
            sql = u"INSERT INTO weibo_users_info (name, fans, followings, url, posts) VALUES ('%s', '%s', '%s', '%s', '%s')" % (user['_id'], user['fensi'], user['guanzhu'], user['url'], user['weibo'])
            sql = sql.encode('utf8')
            cur.execute(sql)

    conn.commit()
    conn.close()





if __name__ == "__main__":
    iname = sys.argv[1]

    crawl(iname)
