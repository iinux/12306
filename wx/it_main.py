# coding=utf8
import itchat
from flask import request, jsonify
import flask
import config
import random
import time
import threading
import signal
import sys


app = flask.Flask(__name__)
stop_continuous_flags = {}


def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()


@itchat.msg_register(itchat.content.TEXT)
def print_message(msg):
    split_msg = msg['Text'].split(':')
    if len(split_msg) >= 2:
        if split_msg[1] == 'ok':
            random_number = int(split_msg[0])
            stop_continuous_flags[random_number] = True
            return 'stop ok'

    print(msg['Text'])


@app.route("/wxpy", methods=['GET', 'POST'])
def index():
    key = request.args.get('key', 0, type=str)
    if key != config.key:
        return jsonify(result='key error')
    content = request.args.get('content', 0, type=unicode)

    who = request.args.get('who', type=unicode)

    interval = request.args.get('interval', default=0, type=int)
    continuous_times = request.args.get('continuous_times', default=1, type=int)

    if interval > 0:
        t = threading.Thread(target=continuous_send, args=(content, who, interval, continuous_times))
        t.setDaemon(True)
        t.start()
    else:
        wechat_send(who, content)

    return jsonify(result='ok')


def continuous_send(content, who, interval, continuous_times):
    random_number = random.randint(1, 10000)
    content = str(random_number) + ':' + content
    while True:
        if random_number in stop_continuous_flags and stop_continuous_flags[random_number]:
            del stop_continuous_flags[random_number]
            break
        wechat_send(who, content)
        continuous_times -= 1
        if continuous_times <= 0:
            break
        time.sleep(interval)


def wechat_run():
    itchat.run()


def wechat_send(who, content):
    if who is None:
        who = u'张群'
    f = itchat.search_friends(who)
    itchat.send(content, f[0]['UserName'])


# 进入Python命令行，让程序保持运行
# embed()
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    itchat.auto_login(hotReload=True)

    t = threading.Thread(target=wechat_run)
    t.setDaemon(True)
    t.start()
    app.run(host=config.flask_listen_host)
