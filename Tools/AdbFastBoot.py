# -*- coding: utf-8 -*-
# coding=utf-8
import os
import subprocess
import threading
import re

# bootloader_image ="bootloader-angler-angler-03.68.img"
# radio_image ='radio-angler-angler-03.81.img'
# update_zip ='image-angler-n2g47o.zip'
bootloader_image ="bootloader-angler-angler-03.79.img"
radio_image ='radio-angler-angler-03.85.img'
update_zip ='image-angler-opm5.171019.015.zip'

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


def operate(cmds):
    for cmd in  cmds:

        excute(cmd)
        excute("sleep 5")
    print('reboot')
    pass


def main():
    connectdevice = get_conn_dev()
    cmds_list =[]



    for device in connectdevice:
        cmds =[]
        adb_cmd = "adb -s %s reboot bootloader" % (device)
        unlock_cmd = "fastboot -s %s flashing unlock" % (device)
        power_cmd ='adb -s %s shell input keyevent 26' % (device)
        flash_image = 'fastboot  -s % s flash bootloader %s'% (device,bootloader_image)
        flash_radio = 'fastboot  -s % s flash radio %s' % (device,radio_image)
        flash_update  = 'fastboot  -s % s -w update %s' % (device,update_zip)
        fast_boot = 'fastboot  -s % s reboot' % (device)
        cmds.append(adb_cmd)
        cmds.append(unlock_cmd)
        cmds.append(power_cmd)
        cmds.append(flash_image)
        cmds.append(flash_radio)
        cmds.append(flash_update)
        cmds.append(fast_boot)
        cmds_list.append(cmds)
    threads = []
    threads_count = len(cmds_list)
    for i in range(threads_count):
       t = threading.Thread(target=operate, args=(cmds_list[i],))
       threads.append(t)
    for i in range(threads_count):
        threads[i].start()
        print("开始刷机",connectdevice[i])
    for i in range(threads_count):
        threads[i].join()

if __name__ == '__main__':
    main()

