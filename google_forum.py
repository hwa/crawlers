#-*- coding: utf-8 -*-

import requests
import bs4
import urllib
from utils import *
from google import *


#
# Single crawling
#

def mk_url(word, begin_date, end_date, entry_begin=None, page=None):
    begin_date = urllib.quote(begin_date, '')
    end_date = urllib.quote(end_date, '')
    word = urllib.quote(word)
    url_ = 'http://www.google.com.hk/search?q=%s&newwindow=1&hl=en&gl=us&as_drrb=b&authuser=0&noj=1&tbs=cdr:1,cd_min:%s,cd_max:%s,sbd:1&tbm=dsc&ei=RJ2EUcWIK8GtiQKAn4GwCQ&start=%d&sa=N&biw=1274&bih=482'
    if entry_begin != None:
        return url_ % (word, begin_date, end_date, entry_begin)
    elif page != None:
        return url_ % (word, begin_date, end_date, page*10)
    else:
        raise Exception("one of entry_begin and page is required")

def get_forum_sparse(begin_date, end_date, word, quote_key=True):
    "搜索两个日期之间的关键词"
    return search_sparse(mk_url, begin_date, end_date, word, quote_key, 'forum')

def get_blogs_dense(begin_date, end_date, word, quote_key=True, density=15):
    return search_dense(mk_url, begin_date, end_date,
                        word, quote_key, density, 'forum')
