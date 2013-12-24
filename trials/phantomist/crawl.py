#!/usr/bin/env python
#-*- coding: utf-8 -*-

import envoy
import os
import sys
import random
import json
import time

def tmp_outfile(samples = '0123456789abcdefghijklmnopqrstuvwxyz',
                length = 20):
    r = ''.join(random.sample(samples, length))
    return os.path.join('/tmp', 'zc-weibo-%s.json' % r)


def crawl_reposts_of(weibo_url):
    """
    """
    def _f():
        script = 'weibo-crawler.js'
        phantomjs = "../vendor/phantomjs-1.8.1-linux-x86_64/bin/phantomjs --web-security=no --cookies-file=cookie --load-images=no %s" % script
        outfile = tmp_outfile()
        r = envoy.run("%s %s %s" % (phantomjs, weibo_url, outfile), timeout=3600)
        if r.status_code == 0:
            with open(outfile, 'r') as rf:
                reposts = json.load(rf)
            envoy.run('rm %s' % outfile)
            return reposts
        elif r.status_code == -15:
            print "timeout: %s" % weibo_url
            return -15
        else:
            raise Exception(r.std_err)
    print 'crawling reposts of weibo: %s' % weibo_url
    reposts = _f()

    if reposts == -15:
        print "retry %s" % weibo_url
        reposts = _f()
        if reposts == -15:
            print "return []"
            return []
        
    reposts = reduce(lambda z, d: z if d in z else z + [d],
                     reposts,
                     [])
    # if len(reposts) == 0:
    #     reposts = _f()
    #     if len(reposts) == 0:
    #         reposts = _f()
    print 'got %d reposts.' % len(reposts)
    return reposts

def try_times(url):
    n = 0
    while n < 3:
        try:
            return crawl_reposts_of(url)
        except Exception as e:
            print "Exception: %s" % e
            print "Retry"
            n += 1
    return []

def recursively_crawl_reposts(seeds):
    def _f(url):
        reposts = try_times(url)
        return (reposts,
                [i['repost-url'] for i in reposts if i['repost-num'] > 0])

    def _g(reposts_tree, next_urls):
        print 'crawling reposts of %d weibo.' % len(next_urls)
        if len(next_urls) == 0:
            return reposts_tree
        nu = []
        for url in next_urls:
            r, n = _f(url + '?type=repost')
            reposts_tree[url] = r
            nu += n
            time.sleep(2)
        nu = list(set(nu))
        return _g(reposts_tree, nu)
    
    return _g({}, seeds)
            


if __name__ == "__main__":
    seeds_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(seeds_file, 'r') as sf:
        seeds = [s.strip().split('?')[0] for s in sf.readlines()] # 去掉链接参数

    reposts_tree = recursively_crawl_reposts(seeds)

    with open(output_file, 'w') as of:
        json.dump(reposts_tree, of)
        print 'dump to output file.'
        


