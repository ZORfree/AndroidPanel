# -*- coding:utf-8 -*-

from utils.Commands import AndroidCommands
import os
import re
import time
from decimal import  Decimal

class APPTool(object):
    """docstring for APPTool"""

    def __init__(self, adb):
        # super(APPTool, self).__init__()
        self._adb = adb
        self.number = "0123456789"
        self.pCpu = 0.00
        self.pTotalTime = 0.00
        self.pTotalTimePro = 0.00
        self.pProCpu = 0.00

#------------------------------------------------------comman part------------------------------------------------------

    def initPID(self,packagename):
        psList = [re.sub(" +", " ", i).split(" ")
                  for i in self._adb.RunShellCommand("ps | findstr %s" % packagename) if i != ""]
        # print("psList:%s"%psList)
        global package_pid_Dict
        package_pid_Dict = {}
        for i in psList:
            package_pid_Dict[i[8]] = i[1]

    def div(self, n1, n2, scale):
        if float(n2):
            return round((float(n1) / float(n2)),scale)
        else:
            return 0

    # def cut(self, num, scale):
    #     scale = 10 ** (-scale)
    #     return (num // scale) * scale

    def pidInfo(self, packagename):
        return package_pid_Dict.get(packagename)

    def uidInfo(self, packagename):
        for i in self._adb.RunShellCommand("dumpsys package %s | findstr userId" % packagename):
            if "userId" in i:
                uid = i.split("=")[1].split(" ")[0]
                if not [j for j in uid if j not in self.number]:
                    return uid
        return None

#------------------------------------------------------CPU part------------------------------------------------------
    def getProcessCpuData(self, mpid):
        # mpid = pidInfo(packagename)
        proCpuList = self._adb.RunShellCommand(
            "cat /proc/%s/stat" % mpid)[0].split(" ")
        procpu = int(proCpuList[13]) + int(proCpuList[14]) + \
            int(proCpuList[15]) + int(proCpuList[16])
        return float(procpu)

    def getTotalTime(self):
        totalTime = 0
        TotalCpuList = re.sub(
            " +", " ", self._adb.RunShellCommand("cat /proc/stat")[0]).split(" ")[1:]
        for i in TotalCpuList:
            totalTime += int(i)
        return  (totalTime, int(TotalCpuList[3]))

    def getTotalCpuUsage(self):
        cpu = 0
        totalTime,freetime = self.getTotalTime()
        cpu = totalTime - freetime
        timev = totalTime - self.pTotalTime
        cpuusage = self.div(((cpu - self.pCpu) * 100.00), timev, 2)
        if cpuusage < 0:
            cpuusage = 0.0
        elif cpuusage > 100:
            cpuusage = 100
        self.pCpu = cpu
        self.pTotalTime = totalTime
        return cpuusage


    def getProcessCpuUsage(self, mpid=None):
        if mpid is None:
            return None
        totalTime, freetime = self.getTotalTime()
        timev = totalTime - self.pTotalTimePro
        newprocpu = self.getProcessCpuData(mpid)
        prousage = self.div(((newprocpu - self.pProCpu) * 100.00), timev, 2)
        if prousage < 0:
            prousage = 0.0
        elif prousage > 100:
            prousage = 100
        self.pProCpu = newprocpu
        self.pTotalTimePro = totalTime
        return  prousage


#------------------------------------------------------RAM part------------------------------------------------------
    def getTotalRamData(self):
        MemTotal, MemFree = None, None
        TotalMemList = [re.sub(" +", " ", i).split(" ")
                        for i in self._adb.RunShellCommand("cat /proc/meminfo") if i != ""]

        MemTotalStr = TotalMemList[0][1]
        if not [j for j in MemTotalStr if j not in self.number]:
            MemTotal = self.div(MemTotalStr, 1024, 2)
        MemFreeInfo = TotalMemList[1][1]
        BuffersInfo = TotalMemList[3][1]
        CachedInfo = TotalMemList[4][1]
        if not [j for j in MemFreeInfo + BuffersInfo + CachedInfo if j not in self.number]:
            Memfree = float(MemFreeInfo) + float(BuffersInfo) + float(CachedInfo)
            Memfree = self.div(Memfree, 1024, 2)
        MemUsage = self.div((MemTotal-Memfree)*100,MemTotal,2)
        return MemTotal, Memfree, MemUsage

    def getProcessRamData(self, mpid):
        proMem = None
        proRamList = self._adb.RunShellCommand(
            "dumpsys meminfo %s |findstr TOTAL" % mpid)
        if not proRamList:
            return None
        try:
            for i in proRamList:
                if i != "":
                    proMemList = re.sub(" +", " ", i).split(" ")
                    proMemStr = proMemList[1]
                    if not [j for j in proMemStr if j not in self.number]:
                        proMem = self.div(proMemStr, 1024, 2)
                        return proMem
        except Exception as e:
            return proMem

#------------------------------------------------------Net part------------------------------------------------------
    def getUidNetBytes(self, muid):
        # muid = uidInfo(packagename)
        proNetRcv, proNetSnd = None, None
        # if [i for i in adb.RunShellCommand("cat /proc/uid_stat/%s/tcp_rcv" % muid) if i!='']
        try:
            proNetRcv = self._adb.RunShellCommand(
                "cat /proc/uid_stat/%s/tcp_rcv" % muid)[0]
            proNetSnd = self._adb.RunShellCommand(
                "cat /proc/uid_stat/%s/tcp_snd" % muid)[0]
        except Exception as e:
            pass
        return proNetRcv, proNetSnd

    def getNetBytes(self, muid=None):
        TotalNetList = [re.sub(" +", " ", i).split(" ") for i in self._adb.RunShellCommand(
            "cat /proc/net/xt_qtaguid/stats")[1:] if i != ""]
        TotalNetDict = {}
        TotalRcv, TotalSnd = 0, 0
        if not TotalNetList:
            return None, None
        try:
            for i in TotalNetList:
                if i[1] != "lo":
                    if i[3] not in TotalNetDict.keys():
                        TotalNetDict[i[3]] = []
                    TotalNetDict[i[3]].append([i[5], i[7]])
            if muid:
                if muid in TotalNetDict:
                    for i in TotalNetDict[muid]:
                        TotalRcv += float(i[0])
                        TotalSnd += float(i[1])
                else:
                    return None, None
            else:
                for v in TotalNetDict.values():
                    for i in v:
                        TotalRcv += float(i[0])
                        TotalSnd += float(i[1])
            return TotalRcv, TotalSnd
        except Exception as e:
            print(e)
            return None, None

    # print(getTotalNetBytes("10255"))
    # def getNetSpeed(packagename):
#------------------------------------------------------IO part------------------------------------------------------
    def getIoData(self, mpid=None):
        ioReadStr, ioWriteStr = None, None
        # if packagename:
        # 	mpid = pidInfo(packagename)
        if not mpid:
            return None, None
        else:
            mpid = "self"
        ioList = [re.sub(" +", " ", i).split(" ")
                  for i in self._adb.RunShellCommand("cat /proc/%s/io" % mpid) if i != ""]
        if not ioList:
            return None, None
        for i in ioList:
            if i[0].startswith("read"):
                ioReadStr = self.div(i[1],1024,0)
            elif i[0].startswith("write"):
                ioWriteStr = self.div(i[1],1024,0)
        return ioReadStr, ioWriteStr

    def getIoStat(self):
        ioReadKb, ioWriteKb = 0, 0
        try:
            ioStatList = [re.sub(" +", " ", i).split(" ")
                          for i in self._adb.RunShellCommand("iostat -d -k")[5:] if i != ""]
            if not ioStatList:
                return None, None
            for i in ioStatList:
                ioReadKb = ioReadKb + int(i[4])
                ioWriteKb = ioWriteKb + int(i[5])
            return ioReadKb, ioWriteKb
        except Exception as e:
            return None, None

#------------------------------------------------------Disk part------------------------------------------------------
    # def getDiskUsage(self):
    #     diskData = [i for i in self._adb.RunShellCommand(
    #         "df /mnt/sdcard/") if i != ""][1]
    #     if not diskData:
    #         return None, None
    #     diskList = re.sub(" +", " ", diskData).split(" ")
    #     totalRom = float(diskList[1])
    #     usedRom = float(diskList[2])
    def formatDiskData(self,diskData):
        if "M" in diskData:
            diskValue = float(diskData[:-1])
            return self.div(diskValue, 1024, 2)
        elif "G" in diskData:
            return float(diskData[:-1])
        else:
            diskValue = float(diskData)
            return self.div(diskValue, 1024 * 1024, 2)

    def getDiskData(self):
        diskData = [i for i in self._adb.RunShellCommand(
            "df /mnt/sdcard/") if i != ""][1]
        if not diskData:
            return None, None, None, None
        diskList = re.sub(" +", " ", diskData).split(" ")
        if len(diskList) < 4:
            return None, None, None, None
        totalRom = self.formatDiskData(diskList[1])
        usedRom = self.formatDiskData(diskList[2])
        freeRom = self.formatDiskData(diskList[3])
        romUsage = self.div(usedRom * 100, totalRom, 0)
        return totalRom, usedRom, freeRom, romUsage

    def getDiskUsage_bak(self):
        try:
            diskData = [i for i in self._adb.RunShellCommand(
                "df /mnt/sdcard/") if i != ""][1]
            diskList = re.sub(" +", " ", diskData).split(" ")
            return int(diskList[4][:-1])
        except:
            return None

#------------------------------------------------------DevInfo part------------------------------------------------------
    def getDevInfo_Bak(self):
        devInfo = [re.sub(" +", " ", i).split("=") for i in self._adb.RunShellCommand("cat /system/build.prop | findstr ro.product.brand") if i != ""][0][1] + \
            " " + [re.sub(" +", " ", i).split("=") for i in adb.RunShellCommand(
                "cat /system/build.prop | findstr ro.product.device") if i != ""][0][1]
        androidVersion = [re.sub(" +", " ", i).split("=") for i in self._adb.RunShellCommand(
            "cat /system/build.prop | findstr ro.build.android") if i != ""][0][1]
        mUnrestrictedScreen = [re.sub(" +", " ", i).split(" ") for i in self._adb.RunShellCommand(
            "dumpsys window |findstr mUnrestrictedScreen") if i != ""][0][1]
        cpuInfo = [re.sub(" +", " ", i).split("=") for i in self._adb.RunShellCommand("cat /system/build.prop | findstr ro.product.cpu.name") if i != ""][0][1] + \
            " " + [re.sub(" +", " ", i).split("=") for i in adb.RunShellCommand(
                "cat /system/build.prop | findstr ro.product.cpu.info") if i != ""][0][1]
        gpuInfo = [re.sub(" +", " ", i).split("=") for i in self._adb.RunShellCommand(
            "cat /system/build.prop | findstr ro.product.gpu.info") if i != ""][0][1]
        buildDate = [re.sub(" +", " ", i).split("=") for i in self._adb.RunShellCommand(
            "cat /system/build.prop | findstr ro.product.build.date") if i != ""][0][1]

        return devInfo, androidVersion, mUnrestrictedScreen, cpuInfo, gpuInfo, buildDate

    def getDevInfo(self):
        devInfo = {}
        devInfoCmd = ["manufacturer", "cpu", "gpu", "build.date", "device"]
        buildPropList =[i for i in self._adb.RunShellCommand("cat /system/build.prop | findstr ro") if i.startswith('ro')]
        if not buildPropList:
            return devInfo
        for i in buildPropList:
            if "=" in i:
                buildProp = re.sub(" +", " ", i).split("=")
            elif ":" in i:
                buildProp = re.sub(" +", " ", i).split(":")
            else:
                continue
            for j in devInfoCmd:
                if j in buildProp[0]:
                    if j in devInfo:
                        continue
                    devInfo[j] = buildProp[1]
        return devInfo


# ------------------------------------------------------FPS part------------------------------------------------------
    def getFpsData(self):
        results = self._adb.RunShellCommand('service call SurfaceFlinger 1013')
        match = re.search('^Result: Parcel\((\w+)', results[0])
        cur_surface = 0
        if match:
            try:
                cur_surface = int(match.group(1), 16)
            except Exception:
                pass
        else:
            pass
        return cur_surface,time.time()


    # if __name__ == "__main__":
    # 	refreshPID()
    # 	while True:
    # 		print getProcessRamData(pidInfo("com.iflytek.xiri")),getTotalRamData()
    # 		print getCpuUsage(pidInfo("com.iflytek.xiri"))
    # 		print getDiskData()
    # 		print getUidNetBytes(uidInfo("com.iflytek.xiri")), getNetBytes()
    # 		print getIoStat(), getIoData(), getIoData(pidInfo("com.iflytek.xiri"))
    # 		print getDevInfo()
    # 		time.sleep(1)
# print(getDevInfo())
# print(getUidNetBytes("com.iflytek.xiri"))
# count = 50
# while count:
# 	count-=1
# 	time.sleep(1)
# 	print(getIoStat())
