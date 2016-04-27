#!/bin/bash

#   文件篡改检查脚本
#   apphome:需要监控的文件目录，web应用程序我们只监控ROOT下面的程序文件
#   md5：生成校验文件的目标路径
#   fcount:记录第一次产生目标文件数量，脚本运行时如果发生文件数量的变更将会告警
#   fcount_now:获取当前的目录文件数量统计
#   使用方法：./md5check.sh >> /tmp/md5.log &

apphome='/eater/self/tomcat-self/webapps/ROOT'
md5='/tmp/md5.txt'

#生成MD5文件
makemd5() {
    find $apphome -type f -print0|xargs -0 md5sum > $md5
 }
 
#校验生成的MD5
checkmd5() {
    fcount_now=`find "$apphome" -type f -print|wc -l`   #获取当前的目录文件数量统计
    fcount=`cat $md5|wc -l` #统计历史目录的文件数
    if [ $fcount_now -ne $fcount ]; #如黑客上传新文件则文件数量将于脚本运行时的数目不一样
    then
      echo '[ERROR] check files count error!'
      find $apphome -type f -print0|xargs -0 md5sum > /tmp/md5diff.txt #如果文件数量不一致则输出一个对比文件
      diff $md5 /tmp/md5diff.txt   #对比两个文件的不同之处
    else  md5sum -c --status $md5   #如果文件数量一致则则校验所有文件MD5值
        if [ $? -ne 0 ];    #如果文件不一致则输出告警日志
        then
           echo "[ERROR] md5 check failed!"
        else
           echo 'md5 check success!!'
        fi
    fi
}

while :
do
if [ -f "$md5" ];then   #如果MD5校验文件存在则校验MD5，如果不存在则生成校验文件
    checkmd5    
    sleep 60
else
    makemd5
    sleep 60
fi
done
