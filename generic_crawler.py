#-*- coding: utf-8 -*-
import time

def crawl_search_engine(mk_url,
                        before_start,
                        rq_dom,
                        extract_entries,
                        has_next_page,
                        page_crawl_interval,
                        uniquify,
                        after_end
                        ):
    before_start()
    print "getting page 1...",
    _, dom = rq_dom(mk_url(page=1))
    entries = extract_entries(dom)
    print 'got.'
    p = 2
    while has_next_page(dom):
        if page_crawl_interval >= 1:
            print 'sleep before crawl next page.'
        time.sleep(page_crawl_interval)
        print "getting page %d..." % p,
        _, dom = rq_dom(mk_url(p))
        entries += extract_entries(dom)
        print 'got.'
        p += 1
    entries_ = uniquify(entries)
    after_end(entries_)
    return entries_
