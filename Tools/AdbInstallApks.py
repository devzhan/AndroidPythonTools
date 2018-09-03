# -*- coding: utf-8 -*-
# coding=utf-8
# 获取设备
import os
import subprocess
import threading
import re
import time

apk_path = "weixin.apk"

def excute(cmd):
    subprocess.Popen(cmd, shell=True)

def get_conn_dev():
    p = os.popen('adb devices')
    outstr = p.read()
    print (outstr)
    connectdeviceid = re.findall(r'(\w+)\s+device\s', outstr)
    print(connectdeviceid)
    return connectdeviceid

def main():
    connectdevice = get_conn_dev()
    commands = []

    for device in connectdevice:
        cmd = "adb -s %s install -r %s" % (device,apk_path)
        commands.append(cmd)

    threads = []
    threads_count = len(commands)

    for i in range(threads_count):
        t = threading.Thread(target = excute, args = (commands[i],))
        threads.append(t)

    for i in range(threads_count):
        time.sleep(1)  # 防止adb连接出错
        threads[i].start()
        print("开始安装设备",connectdevice[i])

    for i in range(threads_count):
        threads[i].join()

if __name__ == '__main__':
    main()

