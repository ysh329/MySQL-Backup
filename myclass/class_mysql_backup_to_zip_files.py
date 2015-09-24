# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_mysql_backup_to_zip_files.py
# Description:

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-24 17:50:39
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import os
################################ PART2 CLASS && FUNCTION ##############################
class get_back_database_name_list(object):

    def __init__(self, mysql_user, mysql_passwd):
        self.con = MySQLdb.connect(host = 'localhost',
                                   user = mysql_user,#'root',
                                   passwd = mysql_passwd,#'931209',
                                   #db = '',
                                   charset = 'utf8')



    def __del__(self):
        self.con.close()



    def get_all_database_name_list(self):
        cursor = self.con.cursor()
        cursor.execute("""SHOW DATABASES""")
        database_name_2d_tuple = cursor.fetchall()
        all_database_name_list = map(lambda database_name_tuple: database_name_tuple[0], database_name_2d_tuple)
        return all_database_name_list



    def filter_database_name_list(self, backup_database_name_list, all_database_name_list, default_existed_database_name_list):
        if backup_database_name_list == []:
            backup_database_name_list = list(set(all_database_name_list) - set(default_existed_database_name_list))
        else:
            backup_database_name_list = list(set(backup_database_name_list) - (set(backup_database_name_list) - set(all_database_name_list)))
        return backup_database_name_list



    def backup_backup_database_name_list(self, backup_database_name_list):

        for database_name in iter(backup_database_name_list):
            os.system("".format())



############################ PART3 CLASS && FUNCTION TEST #############################
default_existed_database_name_list = ['information_schema', 'performance_schema']
backup_database_name_list = []
Backup2ZipFile = get_back_database_name_list(mysql_user = 'root',
                                             mysql_passwd = '931209')


all_database_name_list = Backup2ZipFile.get_all_database_name_list()
print "all_database_name_list:%s" % all_database_name_list
backup_database_name_list = Backup2ZipFile.filter_database_name_list(backup_database_name_list = backup_database_name_list,
                                                                     all_database_name_list = all_database_name_list,
                                                                     default_existed_database_name_list = default_existed_database_name_list)
print "backup_database_name_list:%s" % backup_database_name_list