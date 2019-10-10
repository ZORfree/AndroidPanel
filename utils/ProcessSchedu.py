#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ProcessThread.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/20 18:56   gxrao      1.0         None
'''

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

import time

class ProSchedu(object):
    def __init__(self,adb,proUtil,socketio):
        self.adb = adb
        self.proUtil = proUtil
        self.socketio = socketio
        self.retryTimes_CPU = 6
        self.retryTimes_RAM = 6
        self.retryTimes_NET = 6
        self.retryTimes_IO = 6

    def Start(self):
        self.ProRAM = scheduler.add_job(self.RAM_thread, 'interval', seconds=1)
        self.ProCPU = scheduler.add_job(self.CPU_thread, 'interval', seconds=1)
        self.ProNET = scheduler.add_job(self.NET_thread, 'interval', seconds=1)
        self.ProIO = scheduler.add_job(self.IO_thread, 'interval', seconds=1)
        scheduler.start()

    def removejobs(self):
        print("removejobs")
        for i in scheduler.get_jobs():
            i.remove()
            print("移除一个JOB：" + i.name)

    def state(self):
        return scheduler.state
        # return scheduler.running

    def shutdown(self):
        print("Shutdown")
        scheduler.shutdown(wait=False)

    def pause(self):
        print("pause")
        scheduler.pause()

    def resume(self):
        print("resume")
        scheduler.resume()

    def CPU_thread(self):
        if self.adb.enabled:
            proCpuUsage =  self.proUtil.proCpuUsage()
            if proCpuUsage is None:
                if self.retryTimes_CPU < 0:
                    print ('CPU_thread exit')
                    self.ProCPU.remove()
                self.retryTimes_CPU -= 1
            else:
                self.socketio.emit('server_response',{ 'category':7,'data': proCpuUsage},
                              namespace='/proPage')
    def RAM_thread(self):
        if self.adb.enabled:
            usedMem = self.proUtil.proRamUsage()
            if usedMem:
                self.socketio.emit('server_response',{ 'category':8,'used':usedMem},
                              namespace='/proPage')
            else:
                if self.retryTimes_RAM < 0:
                    print('RAM_thread exit')
                    self.ProRAM.remove()
                self.retryTimes_RAM -= 1

    def IO_thread(self):
        if self.adb.enabled:
            readSpeed, writeSpeed, totalReadKb, totalWriteKb = self.proUtil.proIoSpeed()
            if readSpeed or writeSpeed or totalReadKb or totalWriteKb:
                if totalReadKb > 1000 * 1000:
                    totalReadKb = "%.2f GB" % self.proUtil._device.div(totalReadKb, 1024 * 1024, 2)
                elif totalReadKb > 1000:
                    totalReadKb ="%.2f MB" %  self.proUtil._device.div(totalReadKb, 1024, 2)
                else:
                    totalReadKb = '%d KB' % totalReadKb
                if totalWriteKb > 1000 * 1000:
                    totalWriteKb = "%.2f GB" % self.proUtil._device.div(totalWriteKb, 1024 * 1024, 2)
                elif totalWriteKb > 1000:
                    totalWriteKb ="%.2f MB" %  self.proUtil._device.div(totalWriteKb, 1024, 2)
                else:
                    totalWriteKb = '%d KB' % totalWriteKb

                self.socketio.emit('server_response',{ 'category':10, 'totalRead':totalReadKb, 'totalWrite':totalWriteKb, 'read': readSpeed,'write': writeSpeed,'time': int(round(time.time() * 1000))},
                          namespace='/proPage')
            else:
                if self.retryTimes_IO < 0:
                    print ('IO_thread exit')
                    self.ProIO.remove()
                self.retryTimes_IO -= 1

    def NET_thread(self):
        if self.adb.enabled:
            uploadSpeed, downloadSpeed, TotalRcv, TotalSnd = self.proUtil.proNetSpeed()
            if uploadSpeed or downloadSpeed or TotalRcv or TotalSnd:
                if TotalRcv > 1000 * 1000 * 1000:
                    TotalRcv ="%.2f GB" %  self.proUtil._device.div(TotalRcv, 1024 * 1024 * 1024, 2)
                elif TotalRcv > 1000 * 1000:
                    TotalRcv = "%.2f MB" % self.proUtil._device.div(TotalRcv, 1024 * 1024, 2)
                elif TotalRcv > 1000:
                    TotalRcv ="%.2f KB" %  self.proUtil._device.div(TotalRcv, 1024, 2)
                else:
                    TotalRcv = '%d B' % TotalRcv
                if TotalSnd > 1000 * 1000 * 1000:
                    TotalSnd ="%.2f GB" %  self.proUtil._device.div(TotalSnd, 1024 * 1024 * 1024, 2)
                elif TotalSnd > 1000 * 1000:
                    TotalSnd = "%.2f MB" % self.proUtil._device.div(TotalSnd, 1024 * 1024, 2)
                elif TotalSnd > 1000:
                    TotalSnd ="%.2f KB" %  self.proUtil._device.div(TotalSnd, 1024, 2)
                else:
                    TotalSnd = '%d B' % TotalSnd
                self.socketio.emit('server_response',{ 'category':9, 'TotalRcv':TotalRcv, 'TotalSnd':TotalSnd, 'down': downloadSpeed,'up': uploadSpeed,'time': int(round(time.time() * 1000))},
                              namespace='/proPage')
            else:
                if self.retryTimes_NET < 0:
                    print ('NET_thread exit')
                    self.ProNET.remove()
                self.retryTimes_NET -= 1