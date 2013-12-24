#-*- coding: utf-8 -*-

import requests
import bs4
import datetime
import time

proxies = [None,
           #{'http': 'http://zc:zc2009@144.214.46.12:8080/',
           #'https': 'http://zc:zc2009@144.214.46.12:8080/'},
           {'http': 'http://10.240.0.55:3130/',
            'https': 'http://10.240.0.55:3130/'}]


def rq_dom_simple(url, proxy=None):
    headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'}
    #print 'Request(proxy:%s): %s' % (proxy['http'] if proxy else None, url)
    r = requests.get(url, headers = headers, proxies = proxy)
    dom = bs4.BeautifulSoup(r.content.decode('utf-8', errors='ignore'))
    return r, dom


def is_forbidden(dom):
    return False


def rq_dom(url, proxy_sleep=60, check_forbid=is_forbidden):
    """
    """
    global proxies
    ps = proxies
    for p in ps:
        r, dom = rq_dom_simple(url, p)
        if not check_forbid(dom):
            return r, dom
        else:
            print 'Thresholded proxy: %s' % (p['http'] if p else None)
            proxies = proxies[1:] + [proxies[0]]
            next_p = proxies[0]['http'] if proxies[0] else None
            print 'Switch to proxy: %s' % next_p
    print 'proxies exhausted, sleeping for %d seconds at %s' % (proxy_sleep, datetime.datetime.now())
    time.sleep(proxy_sleep)
    return rq_dom(url, proxy_sleep * 2, check_forbid)
