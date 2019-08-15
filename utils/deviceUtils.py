# -*- coding:utf-8 -*-

from Commands import AndroidCommands
import time
from AppTool import APPTool


class devUtils(object):
    """docstring for devUtils"""

    def __init__(self, device):
        super(devUtils, self).__init__()
        self._device = device
        self.pIotime = 0
        self.pNettime = 0
        self.pRead = 0
        self.pWrite = 0
        self.No1Rcv = 0
        self.No1Snd = 0
        self.pRcv = 0
        self.pSnd = 0
        self.ioSwitch = 1
        self.totalReadKb = 0
        self.totalWriteKb = 0
        self.pFpsCount = 0
        self.pFpsTime = 0

    def devInfo(self):
        deviceInfoDict = self._device.getDevInfo()
        if not deviceInfoDict:
            return [None, None, None, None, None]
        Manufacturer = deviceInfoDict.get("manufacturer")
        device = deviceInfoDict.get("device")
        cpuInfo = deviceInfoDict.get('cpu')
        gpuInfo = deviceInfoDict.get('gpu')
        buildDate = deviceInfoDict.get('build.date')
        return [Manufacturer, device, cpuInfo, gpuInfo, buildDate]

    # def devInfo(self):
    #     Manufacturer, androidVersion, cpuInfo, gpuInfo, buildDate = None, None, None, None, None
    #     deviceInfoDict = self._device.getDevInfo()
    #     androidVersion = deviceInfoDict.get('ro.build.android')
    #     try:
    #         Manufacturer = deviceInfoDict.get(
    #             'ro.product.brand') + " " + deviceInfoDict.get('ro.product.device')
    #         cpuInfo = deviceInfoDict.get(
    #             'ro.product.cpu.name') + " " + deviceInfoDict.get('ro.product.cpu.info')
    #     except Exception as e:
    #         pass
    #     gpuInfo = deviceInfoDict.get('ro.product.gpu.info')
    #     buildDate = deviceInfoDict.get('ro.product.build.date')
    #     return [Manufacturer, androidVersion, cpuInfo, gpuInfo, buildDate]

    def cpuUsage(self):
        return self._device.getCpuUsage()

    def diskUsage(self):
        return self._device.getDiskData()

    def netSpeed(self):
        if not self.pNettime:
            self.pNettime = time.time()
            self.pRcv, self.pSnd = self._device.getNetBytes()
            self.No1Rcv ,self.No1Snd = self.pRcv, self.pSnd
        newtime = time.time()
        timev = newtime - self.pNettime
        self.pNettime = newtime
        rcv, snd = self._device.getNetBytes()
        TotalRcv = rcv - self.No1Rcv
        TotalSnd = snd - self.No1Snd
        rxBytes = rcv - self.pRcv
        seBytes = snd - self.pSnd
        self.pRcv, self.pSnd= rcv, snd
        downloadSpeed = self._device.div(
            rxBytes, timev, 1)
        uploadSpeed = self._device.div(
            seBytes, timev, 1)
        downloadSpeed = self._device.div(downloadSpeed, 1024, 0)
        uploadSpeed = self._device.div(uploadSpeed, 1024, 0)
        if uploadSpeed < 0:
            uploadSpeed = 0
        if downloadSpeed < 0:
            downloadSpeed = 0

        return uploadSpeed, downloadSpeed, TotalRcv, TotalSnd

    def ramUsage(self):
        return self._device.getTotalRamData()

    def ioSpeed(self):
        if not self.pIotime:
            self.pIotime = time.time()
            self.pRead, self.pWrite = self._device.getIoData()
            if not self.pRead:
                self.pRead, self.pWrite = self._device.getIoStat()
                self.ioSwitch = 0
        newtime = time.time()
        timeV = newtime - self.pIotime
        self.pIotime = newtime
        if self.ioSwitch:
            read, write = self._device.getIoData()
        else:
            read, write = self._device.getIoStat()
        if read and self.pRead:
            readKbs = read - self.pRead
            readSpeed = self._device.div(
                readKbs, timeV, 0)
            self.pRead = read
            self.totalReadKb += readKbs
        else:
            readSpeed = 0

        if write and self.pWrite:
            writeKbs = write - self.pWrite
            writeSpeed = self._device.div(
                writeKbs, timeV, 0)
            self.pWrite = write
            self.totalWriteKb += writeKbs
        else:
            writeSpeed = 0
        if readSpeed < 0:
            readSpeed = 0
        if writeSpeed < 0:
            writeSpeed = 0
        return readSpeed, writeSpeed, int(self.totalReadKb), int(self.totalWriteKb)

    def FPSData(self):
        if not self.pFpsTime:
            fpsCount, newTime = self._device.getFpsData()
            self.pFpsCount, self.pFpsTime = fpsCount, newTime
        fpsCount, newTime = self._device.getFpsData()
        timeV = newTime - self.pFpsTime
        thisFps = fpsCount - self.pFpsCount
        self.pFpsCount, self.pFpsTime = fpsCount, newTime
        FPS = self._device.div(
            thisFps, timeV, 1)
        return FPS
