# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: main.py
# Description:

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-24 17:25:54
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import os
import time
import ftplib
import traceback
################################ PART3 MAIN ###########################################
#config vars
#路径分割符，*nix用"/" win32用"\\"
systempathchr="/"

# 数据库用户名
dbuser="root"
# 数据库密码
dbpwd="931209"
#需要备份那些数据库
dbnamelist = []





#本地备份文件夹
workdir="/path/to/backup/"
#错误日志名
errlogfile="databack.log"
#ftp地址
ftp_addr="192.168.0.2"
#ftp端口
ftp_port="2102"
#ftp用户名
ftp_user="databack"
#ftp密码
ftp_pwd="backpwd"
#存放到ftp路径
ftp_path="/"

ftpqueue=[]


def ftpstor():
    #login
    bufsize=1024
    ftp=ftplib.FTP()
    try:
        ftp.connect(ftp_addr,ftp_port)
        ftp.login(ftp_user,ftp_pwd)
        ftp.cwd(ftp_path)
        for filepath in ftpqueue:

            #open file for input as binary
            f=open(filepath,"rb")
            #store file as binary
            print getfilename(filepath)
            ftp.storbinary("STOR "+getfilename(filepath),f,bufsize)
            f.close()
        ftp.quit()
    except:
        path=os.path.join(workdir,errlogfile)
        traceback.print_exc(file=open(path,"a"))



def dumpdb(dbname):
    global ftpqueue
    timeformat="%Y%m%d"
    sqlvalformat="mysqldump -u%s -p\"%s\" \"%s\" >\"%s\""
    tarvalformat="tar --directory=\"%s\" -zcf \"%s\" \"%s\""
    nowdate=time.strftime(timeformat)
    dumpfile=os.path.join(workdir,dbname+".dump")
    zipfile=os.path.join(workdir,dbname+nowdate+".tar.gz")
    sqlval=sqlvalformat % (dbuser,dbpwd,dbname,dumpfile)

    result=os.system(sqlval)
    tarval=tarvalformat % (workdir,zipfile,dbname+".dump")

    result=os.system(tarval)
    os.remove(dumpfile)
    ftpqueue.append(zipfile)

def getfilename(path):

    pt=path.rfind(systempathchr)
    return path[pt+1:]

def main():
    for dbname in dbnamelist:
        dumpdb(dbname)

    ftpstor()

main()