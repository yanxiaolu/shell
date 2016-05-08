#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
request: oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm

'''

import cx_Oracle
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

con = cx_Oracle.connect('bb2/bb2test@DB_IP/dbname')
cur = con.cursor()
cur.execute('''
select rad.xx||'|'||to_char(sysdate-1/24/12,'yyyy-mm-dd hh24:mi')
||'|'||rad.zhtj
||'|'||rec.zhtj
from
(select a.zones as xx,count(r.username) as zhtj from account a,radiuslog r
where a.vlogin_id=r.username and r.authtime > sysdate-1/24/12 and r.authstat='login ok'
group by a.zones) rad,
(select a.zones as xx,count(o.vlogin_id) as zhtj from account a,online_record_work o
where a.vlogin_id=o.vlogin_id and o.dsession_end_date is null
group by a.zones) rec
where rad.xx = rec.xx order by rec.zhtj desc
''')
filename = '/tmp/yxjk'+time.strftime("%Y%m%d%H%M", time.localtime())+'.txt'
print filename
f = open(filename,"a")
for r in cur:
   f.write(r[0].decode('utf-8')+'\n')
f.close()
cur.close()
con.close()
