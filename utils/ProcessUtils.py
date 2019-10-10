#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ProcessUtils.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/20 17:38   gxrao      1.0         None
'''

import time

class proUtils(object):
    def __init__(self,device):
        super(proUtils, self).__init__()
        self._device = device
        self.packagename = None
        self.mUid = None
        self.mPid = None
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
    def proCpuUsage(self):
        self.reFreshLive()
        if not self.mPid:
            return None
        return self._device.getProcessCpuUsage(self.mPid)

    def proRamUsage(self):
        self.reFreshLive()
        if not self.mPid:
            return None
        return self._device.getProcessRamData(self.mPid)

    def proIoSpeed(self):
        self.reFreshLive()
        if not self.mPid:
            return None,None,None,None
        if not self.pIotime:
            self.pIotime = time.time()
            self.pRead, self.pWrite = self._device.getIoData(self.mPid)
            if self.pRead is None:
                self.pIotime = 0
                return None,None,None,None
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

    def proNetSpeed(self):
        self.reFreshLive()
        if not self.mUid:
            return None,None,None,None
        if not self.pNettime:
            self.pNettime = time.time()
            # print (self._device.uidInfo(self.packagename))
            self.pRcv, self.pSnd = self._device.getNetBytes(self.mUid)
            self.No1Rcv ,self.No1Snd = self.pRcv, self.pSnd
        newtime = time.time()
        timev = newtime - self.pNettime
        self.pNettime = newtime
        rcv, snd = self._device.getNetBytes(self.mUid)
        if rcv is None:
            return None,None,None,None
        TotalRcv = rcv - self.No1Rcv
        TotalSnd = snd - self.No1Snd
        rxBytes = rcv - self.pRcv
        seBytes = snd - self.pSnd
        self.pRcv, self.pSnd= rcv, snd
        downloadSpeed = self._device.div(
            rxBytes, timev, 1)
        uploadSpeed = self._device.div(
            seBytes, timev, 1)
        downloadSpeed = self._device.div(downloadSpeed, 1024, 1)
        uploadSpeed = self._device.div(uploadSpeed, 1024, 1)
        if uploadSpeed < 0:
            uploadSpeed = 0
        if downloadSpeed < 0:
            downloadSpeed = 0

        return uploadSpeed, downloadSpeed, TotalRcv, TotalSnd

    def reFreshLive(self):
        # if self.packagename:
        #     pUid = self.mUid
        #     self.mUid = self._device.uidInfo(self.packagename)
        #     if pUid:
        #         if self.mUid != pUid:
        #             self._device.initPID()
        #     self.mPid = self._device.pidInfo(self.packagename)
        if self.packagename:
            pPid = self.mPid
            self._device.initPID(self.packagename)
            self.mPid = self._device.pidInfo(self.packagename)
            if self.mPid:
                if self.mPid != pPid:
                    self.mUid = self._device.uidInfo(self.packagename)



    def setPackageName(self,packagename):
        self.packagename = packagename


