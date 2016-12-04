#-*- coding:utf-8 -*-

from  wxsdk import *
import re
import os
import time
import sys

file_path = '/Users/YANXL/OneDrive/Code/test.sh'
key_words = {'Connection refused','timed out'}

def logcheck():
    wx = wxsdk()
    f = open(file_path,'r')
    #f.seek(0,2)
    watcher = os.stat(file_path)
    this_modified = last_modified = watcher.st_mtime
    #while 1:
    #if this_modified > last_modified:
    #    last_modified = this_modified
    while 1:
        line = f.readline()
        if not line: break
        for keyword in key_words:
            #print line
            if re.search(keyword,line):
                status,res = wx.sendmsg(touser='yanxl',content='日志中出现[%s]！'%keyword)
    #watcher = os.stat(file_path)
    #this_modified = watcher.st_atime
    #time.sleep(3)

    print status, res
    return
if __name__=='__main__':
    logcheck()
