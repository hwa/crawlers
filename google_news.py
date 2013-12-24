#-*- coding: utf-8 -*-

import requests
import bs4
import urllib
from utils import *
from google import *

def extract_entries(dom):
    def _f(td):
        title = td.find('h3',class_='r').text
        url = td.find('h3',class_='r').find('a')['href']
        try:
            source_, pub_date_ = td.find('div',class_='slp').find_all('span',class_='nsa')
        except ValueError:
            source_ = td.find('div', class_='slp').find('span', class_='news-source')
            pub_date_ = td.find('div', class_='slp').find('span', class_='nsa')
        source, pub_date = source_.text, pub_date_.text
        summary = dom.find('td',class_='tsw').find('div',class_='st').text
        return {'title': title,
                'url': url,
                'source': source,
                'pub_date': pub_date,
                'summary': summary}
    return map(_f, dom.find_all('td', class_='tsw'))


#
# Single crawling
#

def mk_url(word, begin_date, end_date, entry_begin):
    begin_date = urllib.quote(begin_date, '')
    end_date = urllib.quote(end_date, '')
    word = urllib.quote(word)
    return 'http://www.google.com.hk/search?q=%s&newwindow=1&hl=en&gl=us&as_drrb=b&authuser=0&noj=1&tbs=cdr:1,cd_min:%s,cd_max:%s,sbd:1&tbm=nws&ei=RJ2EUcWIK8GtiQKAn4GwCQ&start=%d&sa=N&biw=1274&bih=482' % (word, begin_date, end_date, entry_begin)

def get_news_sparse(begin_date, end_date, word, quote_key=True):
    """
    搜索两个日期之间的关键词
    """
    return search_sparse(mk_url,
                         begin_date, end_date, word,
                         quote_key,
                         name='news',
                         extract_entries=extract_entries)

def get_news_dense(begin_date, end_date, word, quote_key=True, density=15):
    "搜索两个日期之间，以一段时间为精度的逐一搜索"
    return search_dense(mk_url, begin_date, end_date, word,
                        quote_key, density,
                        name='news',
                        extract_entries=extract_entries)
