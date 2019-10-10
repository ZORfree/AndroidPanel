# -*- coding:utf-8 -*-
import subprocess
from utils.Commands import AndroidCommands
import os
from datetime import datetime
import time
from utils.AppTool import APPTool
from utils.DeviceUtils import devUtils
from utils.ProcessUtils import proUtils
from utils.Logcat import LOGCAT
from utils.Script import SCRIPT
from threading import Thread
from utils.ProcessSchedu import ProSchedu
if __name__ == "__main__":

    deviceName = os.popen('adb devices').readlines()[1].split()[0]
    adb = AndroidCommands(deviceName)
    device = APPTool(adb)
    # devUtil = devUtils(device)
    proUtil = proUtils(device)
    proUtil.setPackageName('com.iflytek.xiri')
    while adb.enabled:
        proCpuUsage = proUtil.proCpuUsage()
        print(proCpuUsage)
        print(proCpuUsage is None)
        # time.sleep(1)
    # script = SCRIPT(adb)
    # print("初始化时：%d" %script.state())
    # now = int(time.time())
    # jobList = [
    #     {"fun":script.Playback ,"inv":6,"start_date":datetime.fromtimestamp(now),"end_date":datetime.fromtimestamp(now+20)},
    #     {"fun": script.Keydown,"run_date":datetime.fromtimestamp(now+25),"arg":[3]},
    #     {"fun": script.Live,"inv":15,"start_date":datetime.fromtimestamp(now+30),"end_date":datetime.fromtimestamp(now+70)},
    #     {"fun": script.Keydown,"run_date": datetime.fromtimestamp(now + 75),"arg":[3]},
    #     {"fun": script.Vod, "inv": 6, "start_date": datetime.fromtimestamp(now + 80),"end_date": datetime.fromtimestamp(now + 100)},
    #     {"fun": script.Keydown,"run_date": datetime.fromtimestamp(now + 105),"arg":[3]},
    #     {"fun": script.Skill, "inv": 5, "start_date": datetime.fromtimestamp(now + 110),
    #      "end_date": datetime.fromtimestamp(now + 130)},
    #     {"fun": script.Keydown,"run_date": datetime.fromtimestamp(now + 135),"arg":[3]},
    # ]
    #
    # script.Add_Job(jobList)
    # script.Start()
    # print("添加JOB后：%d" %script.state())
    # time.sleep(20)
    # script.pause()
    # print("暂停后：%d" %script.state())
    # time.sleep(20)
    # script.resume()
    # print("恢复后：%d" %script.state())
    # time.sleep(20)
    # script.removejobs()
    # print("移除后：%d" % script.state())
    # time.sleep(20)
    # script.shutdown()
    # print("关闭后：%d" %script.state())
    # time.sleep(140)


    # mPid = device.pidInfo("com.iflytek.xiri")
    # print(mPid)
    # print(proUtil.packagename)
    # proUtil.reFreshLive()
    # print(proUtil.mPid)
    # print (proUtil.proCpuUsage())
    # print (proUtil.proIoSpeed())
    # print (proUtil.proRamUsage())
    # print (proUtil.proNetSpeed())

    # while True:
        # proUtil.proCpuUsage()
        # print (proUtil.proCpuUsage())
        # print (proUtil.proRamUsage())
        # time.sleep(1)

    # devUtil = devUtils(device)
    #
    # print (device.getIoData())
    # print (devUtil.devInfo())
    # print (devUtil.cpuUsage())
    # print (devUtil.FPSData())
    # print (devUtil.netSpeed())
    # print (devUtil.diskUsage())
    # print (devUtil.ramUsage())
    # count = 50
    # while 1:
    #     time.sleep(1)
    #     print(devUtil.cpuUsage())

    # while True:
    #     time.sleep(2)
    #     fps_List = []
    #     for i in range(15):
    #         fps = devUtil.FPSData()
    #         if fps:
    #             fps_List.append(fps)
    #     if fps_List:
    #         print sum(fps_List) / len(fps_List)


