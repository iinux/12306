# coding=utf8
from wxpy import *
from flask import request, jsonify
import flask
import config
import random
import time
import threading

app = flask.Flask(__name__)
bot = Bot(cache_path=True)
my_friend = bot.friends().search(u'张群', sex=MALE)[0]
stop_continuous_flags = {}


@app.route("/wxpy", methods=['GET', 'POST'])
def index():
    key = request.args.get('key', 0, type=str)
    if key != config.key:
        return jsonify(result='key error')
    content = request.args.get('content', 0, type=unicode)

    who = request.args.get('who', type=unicode)
    if who is not None:
        a_friend = bot.friends().search(who)[0]
    else:
        a_friend = my_friend

    interval = request.args.get('interval', default=0, type=int)
    continuous_times = request.args.get('continuous_times', default=1, type=int)

    if interval > 0:
        t = threading.Thread(target=continuous_send, args=(content, a_friend, interval, continuous_times))
        t.start()
    else:
        a_friend.send(content)

    return jsonify(result='ok')


def continuous_send(content, a_friend, interval, continuous_times):
    random_number = random.randint(1, 10000)
    content = str(random_number) + ':' + content
    while True:
        if random_number in stop_continuous_flags and stop_continuous_flags[random_number]:
            del stop_continuous_flags[random_number]
            break
        a_friend.send(content)
        continuous_times -= 1
        if continuous_times <= 0:
            break
        time.sleep(interval)


@bot.register()
def print_message(msg):
    split_msg = msg.text.split(':')
    if len(split_msg) >= 2:
        if split_msg[1] == 'ok':
            random_number = int(split_msg[0])
            stop_continuous_flags[random_number] = True

    print(msg.text)
    # return msg.text


# bot.file_helper.send("hello")
# 发送文本给好友
# my_friend.send('Hello WeChat!')
# 发送图片
# my_friend.send_image('my_picture.jpg')

# 进入Python命令行，让程序保持运行
# embed()
if __name__ == "__main__":
    app.run(host=config.flask_listen_host)
