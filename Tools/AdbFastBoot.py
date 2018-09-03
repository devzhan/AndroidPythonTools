# -*- coding: utf-8 -*-
# coding=utf-8
# 获取设备
import os
import subprocess
import threading
import re
import time


def excute(cmd):
    p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    out = p.stdout.readlines()
    print(out)
    print("cmd is :",cmd)

def get_conn_dev():
    p = os.popen('adb devices')
    outstr = p.read()
    print (outstr)
    connectdeviceid = re.findall(r'(\w+)\s+device\s', outstr)
    print(connectdeviceid)
    return connectdeviceid


def operate(param, param1, param2, param3, param4,param5,param6):
    excute(param)
    excute("sleep 5")
    excute(param1)
    excute("sleep 5")
    excute(param2)
    excute("sleep 5")
    excute(param3)
    excute("sleep 5")
    excute(param4)
    excute("sleep 5")
    excute(param5)
    excute("sleep 5")
    print('over')
    excute(param6)
    print('reboot')
    pass


def main():
    connectdevice = get_conn_dev()
    adb_commands = []
    unlock_commands = []
    image_commands = []
    radio_commands = []
    update_commands = []
    power_cmds = []
    reboot_cmds =[]




    for device in connectdevice:
        adb_cmd = "adb -s %s reboot bootloader" % (device)
        unlock_cmd = "fastboot -s %s flashing unlock" % (device)
        power_cmd ='adb -s %s shell input keyevent 26' % (device)
        flash_image = 'fastboot  -s % s flash bootloader bootloader-angler-angler-03.68.img'%(device)
        flash_radio = 'fastboot  -s % s flash radio radio-angler-angler-03.81.img'%(device)
        flash_update  = 'fastboot  -s % s -w update image-angler-n2g47o.zip'%(device)
        fast_boot = 'fastboot  -s % s reboot' % (device)
        adb_commands.append(adb_cmd)
        unlock_commands.append(unlock_cmd)
        power_cmds.append(power_cmd)
        image_commands.append(flash_image)
        radio_commands.append(flash_radio)
        update_commands.append(flash_update)
        reboot_cmds.append(fast_boot)

    threads = []
    threads_count = len(adb_commands)
    print(unlock_commands)
    for i in range(threads_count):
       # operate(adb_commands[i],unlock_cmd[i],image_commands[i],radio_commands[i],update_commands[i])
       t = threading.Thread(target=operate, args=(adb_commands[i],unlock_commands[i],power_cmds[i],image_commands[i],radio_commands[i],update_commands[i],reboot_cmds[i]),)
       threads.append(t)





    for i in range(threads_count):
        # time.sleep(1)  # 防止adb连接出错
        threads[i].start()
        print("开始刷机",connectdevice[i])

    for i in range(threads_count):
        threads[i].join()

if __name__ == '__main__':
    main()

