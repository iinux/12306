#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from sys import argv
import MySQLdb
import config


db = None
cursor = None


def init_db():
    # 打开数据库连接
    global db
    global cursor
    db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
    db.set_character_set('utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()


def insert_ip(ip):
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT * from ips where ip='%s'" % ip)

    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()
    if data is None:
        try:
            # 执行sql语句
            cursor.execute(
                """INSERT INTO ips(ip) VALUES ('%s')""" % ip)
            # 提交到数据库执行
            db.commit()
        except Exception, e:
            print(e)
            # 发生错误时回滚
            db.rollback()


def insert_user_agent(user_agent):
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT * from user_agents where user_agent='%s'" % user_agent)

    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()
    if data is None:
        try:
            # 执行sql语句
            cursor.execute(
                """INSERT INTO user_agents(user_agent) VALUES ('%s')""" % user_agent)
            # 提交到数据库执行
            db.commit()
        except Exception, e:
            print(e)
            # 发生错误时回滚
            db.rollback()


def parse_log_file(file_name):
    f = open(file_name, 'r')
    while True:
        log_line = f.readline()

        if log_line == "":
            break

        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP address
               '\[(.+)\]\s'  # datetime
               '"GET\s(.+)\s\w+/.+"\s'  # requested file
               '(\d+)\s'  # status
               '(\d+)\s'  # bandwidth
               '"(.+)"\s'  # referrer
               '"(.+)"'  # user agent
               )
        requests = find(pat, log_line)
        if requests:
            for request in requests:
                print type(request[0])
                insert_ip(request[0])
                print (request[0])
                print type(request[6])
                insert_user_agent(request[6])
                print (request[6])


def find(pat, text):
    match = re.findall(pat, text)
    if match:
        return match
    return False


if __name__ == '__main__':
    argv_len = argv.__len__()
    i = 1

    init_db()

    while i < argv_len:
        filename = argv[i]
        i += 1
        parse_log_file(filename)
