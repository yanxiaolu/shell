#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
日期：2016-5-8
需求： 
ftp目录：./data
运行环境需求: oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
              Python 2.6

'''

import cx_Oracle
import time as t
from datetime import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
def fremove(datadir):
    if datetime.today().isoweekday() == 4:
        for r in os.listdir(datadir):
            datafile = os.path.join(datadir, r)
            if datetime.today().replace(day=1) > datetime.fromtimestamp(os.path.getctime(datafile)):
                os.remove(datafile)

def rad_mo(filename,logfile):
    f = open(filename,"w")
    l = open(logfile,"a")
    starttime = t.time()
    con = cx_Oracle.connect('username/Password@localhost/dbName')
    cur = con.cursor()
    cur.execute('''
    select rad.xx||'|'||to_char(sysdate-1/24/12,'yyyy-mm-dd hh24:mi')
    ||'|'||rad.zhtj||'|'||rec.zhtj from
    (select a.zones as xx,count(r.username) as zhtj from account a,radiuslog r
    where a.vlogin_id=r.username and r.authtime > sysdate-1/24/12 and r.authstat='login ok'
    group by a.zones) rad,
    (select a.zones as xx,count(o.vlogin_id) as zhtj from account a,online_record_work o
    where a.vlogin_id=o.vlogin_id and o.dsession_end_date is null
    group by a.zones) rec
    where rad.xx = rec.xx order by rec.zhtj desc
    ''')
    for r in cur:
        f.write(r[0]+'\n')
    elapsed = (t.time()-starttime)
    l.write('elapsed:'+str(elapsed)+'\n')
    l.write('close file.... \n')
    f.close()
    l.write('close cursor... \n')
    cur.close()
    l.write('close connection... \n')
    con.close()
    l.write('wating 300 secend... ...\n')

if __name__=="__main__":
    datadir = '/eater/radius_mo.d/data/'
    logfile = '/eater/radius_mo.d/log/yxjk.log'
    while True:
        filename = '/eater/radius_mo.d/data/yxjk'+datetime.today().strftime('%Y%m%d%H%M')+'.txt'
        fremove(datadir)
        rad_mo(filename,logfile)
        t.sleep(300)
