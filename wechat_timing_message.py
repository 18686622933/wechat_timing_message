#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from wxpy import *
import datetime
import time
from threading import Timer

# 配置信息，额外需要配置下34行发送信息
config = {
    "send_time": "7:00",  # 定时发送时间
    "send_interval": 86400,  # 间隔时间
    "send_targer": "英雄联盟",  # 发送目标 
    "is_cache": True,  # 微信是否缓存登陆（不用重复扫码）
    "2D_code_size": 1,  # 二维码尺寸，在终端中设置为1，在pycharm中设置为2
}


class RepeatingTimer(Timer):
    """用于创建多线程的类"""

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


def begin():
    print("第一次执行")


def func(friend):
    def send_message(role):
        message = "本人及家属身体健康"  # 发送信息
        role.send(message)
        print(role, message)

    try:
        role = bot.friends().search(friend)[0]
        send_message(role)
    except IndexError:
        role = bot.groups().search(friend)[0]
        send_message(role)


def timer_start(spacing=10, **arg):
    """
    执行非阻隔进程定时任务
    :param spacing: 间隔时间，单位秒
    :param arg: func函数的参数
    :return:
    """
    if arg:
        t = RepeatingTimer(spacing, func, args=[arg["arg"]])
    else:
        t = RepeatingTimer(spacing, func)
    t.start()


def align(minute_or_second='s'):
    """
    查询当前时间与整点(或整分钟)时间相差多久，使用time.sheep来等待到整点(或整分钟)时间
    :param minute_or_second: 整点则 ='m' 整分钟则 ='s'
    :return:
    """
    now_time = datetime.datetime.now()
    now_second = now_time.second
    now_minute = now_time.minute
    now_hour = now_time.hour

    next_hour = (datetime.timedelta(hours=1) + datetime.datetime.now()).hour
    next_minute = str(datetime.timedelta(minutes=1) + datetime.datetime.now())[11:16]

    difference_minute = 60 - int(now_minute) - 1
    difference_second = 60 - int(now_second)

    if minute_or_second == 'm':
        if now_second != 0:
            print("当前时间:%s, 距 %s:00:00 点还差 %sm%ss" % (
                str(now_time)[:19], next_hour, difference_minute, difference_second))
        else:
            difference_minute += 1
            print("当前时间:%s, 距 %s:00 点还差 %sm%ss" % (str(now_time)[:19], next_hour, difference_minute, 0))
        time.sleep(difference_minute * 60 + difference_second)
    else:
        print("当前时间:%s, 距 %s:00 点还差 %ss" % (str(now_time)[:19], next_minute, difference_second))
        time.sleep(difference_second)


def wait_time(target):
    """
    :param target: 目标时间
    :return: 下一次到目标时间所有时间（单位：秒）
    """
    now_time = datetime.datetime.now()
    today = str(now_time)[:10]
    target_time = datetime.datetime.strptime("%s %s:00" % (today, target), "%Y-%m-%d %H:%M:%S")
    if now_time > target_time:
        difference = target_time + datetime.timedelta(days=1) - now_time
        print("距离第一次执行还有:%s" % difference)
        return difference.seconds
    elif now_time < target_time:
        difference = target_time - now_time
        print("距离第一次执行还有:%s" % difference)
        return difference.seconds


bot = Bot(cache_path=config["is_cache"], console_qr=config["2D_code_size"])
# cache_path:启动缓存，不用每次都扫码；console_qr:在终端中展示二维码，默认尺寸为2

first_time = config["send_time"]  # 定时发送时间
first_wait_send = wait_time(first_time)
t1 = Timer(first_wait_send, begin)
t1.start()

t1.join()
timer_start(spacing=config["send_interval"], arg=config["send_targer"])  # 间隔时间86400秒，发送对象"英雄联盟"

embed()
