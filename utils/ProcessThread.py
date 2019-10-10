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

# import lib

import time
class ProThread(object):
    def __init__(self, adb,proUtil,socketio):
        self.adb = adb
        self.proUtil = proUtil
        self.socketio = socketio
        self.retryTimes = 6

    def CPU_thread(self):
        count =  self.retryTimes
        while  self.adb.enabled:
            self.socketio.sleep(1)
            proCpuUsage =  self.proUtil.proCpuUsage()
            if proCpuUsage is None:
                print("proCpuUsage: "+proCpuUsage)
                if count < 0:
                    print ('CPU_thread exit')
                    break
                count -= 1
            else:
                self.socketio.emit('server_response',{ 'category':7,'data': proCpuUsage},
                              namespace='/proPage')
        print("P_CPU_thread Exit")
    def RAM_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            self.socketio.sleep(1)
            usedMem = self.proUtil.proRamUsage()
            if usedMem:
                # print ({ 'RAM':usedMem})
                self.socketio.emit('server_response',{ 'category':8,'used':usedMem},
                              namespace='/proPage')
            else:
                if count < 0:
                    print ('RAM_thread exit')
                    break
                count -= 1
        print("P_RAM_thread Exit")
    def IO_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            self.socketio.sleep(1)
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
                # print ({ 'category':'IO', 'totalRead':totalReadKb, 'totalWrite':totalWriteKb, 'read': readSpeed,'write': writeSpeed,'time': int(round(time.time() * 1000))})
                self.socketio.emit('server_response',{ 'category':10, 'totalRead':totalReadKb, 'totalWrite':totalWriteKb, 'read': readSpeed,'write': writeSpeed,'time': int(round(time.time() * 1000))},
                          namespace='/proPage')
            else:
                if count < 0:
                    print ('IO_thread exit')
                    break
                count -= 1
        print("P_IO_thread Exit")
    def NET_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            self.socketio.sleep(1)
            try:
                uploadSpeed, downloadSpeed, TotalRcv, TotalSnd = self.proUtil.proNetSpeed()
            except Exception as e:
                print (e)
                self.socketio.sleep(1)
                continue
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
                # print ({ 'category':'NET', 'TotalRcv':TotalRcv, 'TotalSnd':TotalSnd, 'down': downloadSpeed,'up': uploadSpeed,'time': int(round(time.time() * 1000))})
                self.socketio.emit('server_response',{ 'category':9, 'TotalRcv':TotalRcv, 'TotalSnd':TotalSnd, 'down': downloadSpeed,'up': uploadSpeed,'time': int(round(time.time() * 1000))},
                              namespace='/proPage')
            else:
                if count < 0:
                    print ('NET_thread exit')
                    break
                count -= 1
        print("P_NET_thread Exit")