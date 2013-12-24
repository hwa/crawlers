#-*- coding: utf-8 -*-
from utils import *
import unittest
import generic_crawler
import connect

#
# generic cralwer
#

# search engine crawler

def test(fn):
    def _f():
        print '\n-----',
        print fn.func_name,
        print '-----'
        fn()
    return _f

@test
def test_crawl_search_engine():
    d = {'page': 1}
    def _has_next_page(dom):
        printf('running has_next_page')
        if d['page'] >= 2:
            return False
        else:
            d['page'] += 1
            return True
    generic_crawler.crawl_search_engine(
        lambda page: printf('running mk_url') ,
        lambda : printf('running before_start'),
        lambda u: printf('runnning rq_dom') or (None,None),
        lambda d: printf('running extract_entries') or [],
        _has_next_page,
        1,
        lambda es: es,
        lambda es: printf('running after_end')
        )



def run():
    test_crawl_search_engine()
