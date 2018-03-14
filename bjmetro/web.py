#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask
from flask import request, render_template
import MySQLdb
import config
import sys

sys.path.append('../')
import my_helper

if not my_helper.PY3:
    reload(sys)
    sys.setdefaultencoding('utf8')

app = flask.Flask(__name__)


@app.route("/")
def index():
    db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
    db.set_character_set('utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    query_update_at = request.args.get('update_at')

    cursor.execute("select distinct(update_at) from bj_metro_real_data order by update_at desc limit 100")
    # 使用 fetchone() 方法获取一条数据库。
    all_update_at = cursor.fetchall()
    newest_time = all_update_at[0][0].strftime('%Y-%m-%d %H:%M')

    return_string = ""
    return_string += newest_time + "<br />"

    if query_update_at:
        cursor.execute("select * from bj_metro_real_data where update_at='%s'" % (query_update_at))
    else:
        cursor.execute("select * from bj_metro_real_data where update_at='%s'" % (newest_time))
    data = cursor.fetchall()

    _all_update_at = []
    for update_at in all_update_at:
        update_at = update_at[0].strftime('%Y-%m-%d %H:%M')
        _all_update_at.append(update_at)

    db.close()

    return render_template('index.html', all_update_at=_all_update_at, data=data)


if __name__ == "__main__":
    app.debug = config.flask_debug_switch
    app.run(host=config.flask_listen_host)
