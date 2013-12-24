#-*- coding: utf-8 -*-

import sqlite3



def save_dicts(dicts, db, tbl_name, fields):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS %s' % tbl_name)
    cur.execute('CREATE TABLE %s (%s)' % (tbl_name,
                                          ', '.join([i+' '+j for i,j in fields])))
    for d in dicts:
        vs = [unicode(d[i]).replace("'", "''") for i,j in fields]
        fs = [f[0] for f in fields]
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (tbl_name,
                                                   ', '.join(fs),
                                                   ', '.join(["'%s'" % v for v in vs])
                                                   )
        sql = sql.encode('utf-8')
        cur.execute(sql)

    conn.commit()
    conn.close()
