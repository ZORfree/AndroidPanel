# -*- coding:utf-8 -*-

from Commands import AndroidCommands
import os
import datetime
import time
from AppTool import APPTool
from deviceUtils import devUtils


if __name__ == "__main__":

    deviceName = os.popen('adb devices').readlines()[1].split()[0]
    adb = AndroidCommands(deviceName)
    diskData = adb.RunShellCommand(
        "df /mnt/sdcard/")
    # device = APPTool(adb)
    # devUtil = devUtils(device)

    # print device.getIoData()
    # print devUtil.devInfo()
    # print devUtil.cpuUsage()
    # print devUtil.FPSData()
    # print devUtil.netSpeed()
    # print devUtil.diskUsage()
    # print devUtil.ramUsage()
    # count = 50
    # while 1:
    # 	time.sleep(1)
    #     print devUtil.netSpeed()
    # print datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    # print time.time()

    # while True:
    #     time.sleep(2)
    #     fps_List = []
    #     for i in range(15):
    #         fps = devUtil.FPSData()
    #         if fps:
    #             fps_List.append(fps)
    #     if fps_List:
    #         print sum(fps_List) / len(fps_List)


