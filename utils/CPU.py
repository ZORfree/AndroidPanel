# -*- coding:utf-8 -*-

from Commands import AndroidCommands
import re
import os

deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)
# print(deviceName)
def getIoStat():
    ioReadKb, ioWriteKb = 0, 0
    try:
        ioStatList = [re.sub(" +", " ", i).split(" ")
                      for i in adb.RunShellCommand("iostat -d -k")[5:] if i != ""]
        if not ioStatList:
            return None, None
        for i in ioStatList:
            ioReadKb = ioReadKb + int(i[4])
            ioWriteKb = ioWriteKb + int(i[5])
        return ioReadKb, ioWriteKb
    except Exception as e:
        return None, None

print getIoStat()
