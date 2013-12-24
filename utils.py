#-*- coding: utf-8 -*-

import datetime

def unique(seq, get_key):
    return reduce(lambda (k,z),i: (k,z) if get_key(i) in k else (k+[get_key(i)], z+[i]),
                  seq,
                  ([],[]))[1]

def printf(x):
    print x

#date and time

def cut_dates(date1, date2, interval):
    """
    计算两个日期之间相隔某段时间的所有日期
    """
    ds = [date1]
    d = date1 + datetime.timedelta(interval)
    while d < date2:
        ds.append(d)
        d += datetime.timedelta(interval)
    return ds+[date2]
