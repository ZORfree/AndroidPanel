#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Thread.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/20 14:26   gxrao      1.0         None
'''

from utils.Commands import AndroidCommands
from utils.AppTool import APPTool
from utils.DeviceUtils import devUtils
import time
class Thread(object):
    def __init__(self, adb,devUtil,socketio):
        self.adb = adb
        self.devUtil = devUtil
        self.socketio = socketio
        self.retryTimes = 6

    def CPU_thread(self):
        count =  self.retryTimes
        while  self.adb.enabled:
            cpuUsage =  self.devUtil.cpuUsage()
            if cpuUsage:
                self.socketio.emit('server_response',{ 'category':1,'data': '%.2f' %cpuUsage},
                              namespace='/showPage')
                self.socketio.sleep(1)
            else:
                if count < 0:
                    print ('CPU_thread exit')
                    break
                count -= 1
        print("T_CPU_thread Exit")
    def RAM_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            MemTotal, Memfree, MemUsage = self.devUtil.ramUsage()
            if MemUsage:
                self.socketio.emit('server_response',{ 'category':2,'total': MemTotal,'free':Memfree,'usage':MemUsage},
                              namespace='/showPage')
                self.socketio.sleep(1)
            else:
                if count < 0:
                    print ('RAM_thread exit')
                    break
                count -= 1
        print("T_RAM_thread Exit")
    def FPS_thread(self):
        while self.adb.enabled:
            fps_List = []
            for i in range(15):
                try:
                    fps = self.devUtil.FPSData()
                except Exception as e:
                    print (e)
                    continue
                if fps:
                    fps_List.append(fps)
            if fps_List:
                FPS = self.devUtil._device.div(sum(fps_List), len(fps_List),1)
                cent = self.devUtil._device.div(FPS,60,2) * 100
                self.socketio.emit('server_response',{ 'category':3,'value':FPS, 'cent':cent},
                              namespace='/showPage')
        print("T_FPS_thread Exit")
    def DISK_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            totalRom, usedRom, freeRom, romUsage = self.devUtil.diskUsage()
            # romUsage = devUtil.diskUsage()
            if romUsage:
                self.socketio.emit('server_response',{ 'category':4,'text': str(usedRom)+"/"+str(totalRom)+'G','value':romUsage},
                              namespace='/showPage')
                # socketio.emit('server_response',{'category': 4, 'value': romUsage})
                self.socketio.sleep(5)
            else:
                if count < 0:
                    print ('DISK_thread exit')
                    break
                count -= 1
        print("T_DISK_thread Exit")
    def IO_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            readSpeed, writeSpeed, totalReadKb, totalWriteKb = self.devUtil.ioSpeed()
            self.socketio.sleep(1)
            if readSpeed or writeSpeed or totalReadKb or totalWriteKb:
                if totalReadKb > 1000 * 1000:
                    totalReadKb = "%.2f GB" % self.devUtil._device.div(totalReadKb, 1024 * 1024, 2)
                elif totalReadKb > 1000:
                    totalReadKb ="%.2f MB" %  self.devUtil._device.div(totalReadKb, 1024, 2)
                else:
                    totalReadKb = '%d KB' % totalReadKb
                if totalWriteKb > 1000 * 1000:
                    totalWriteKb = "%.2f GB" % self.devUtil._device.div(totalWriteKb, 1024 * 1024, 2)
                elif totalWriteKb > 1000:
                    totalWriteKb ="%.2f MB" %  self.devUtil._device.div(totalWriteKb, 1024, 2)
                else:
                    totalWriteKb = '%d KB' % totalWriteKb
                self.socketio.emit('server_response',{ 'category':6, 'totalRead':totalReadKb, 'totalWrite':totalWriteKb, 'read': readSpeed,'write': writeSpeed,'time': int(round(time.time() * 1000))},
                          namespace='/showPage')
            else:
                if count < 0:
                    print ('IO_thread exit')
                    break
                count -= 1
        print("T_IO_thread Exit")
    def NET_thread(self):
        count = self.retryTimes
        while self.adb.enabled:
            self.socketio.sleep(1)
            try:
                uploadSpeed, downloadSpeed, TotalRcv, TotalSnd = self.devUtil.netSpeed()
            except Exception as e:
                print (e)
                continue
            if uploadSpeed or downloadSpeed or TotalRcv or TotalSnd:
                if TotalRcv > 1000 * 1000 * 1000:
                    TotalRcv ="%.2f GB" %  self.devUtil._device.div(TotalRcv, 1024 * 1024 * 1024, 2)
                elif TotalRcv > 1000 * 1000:
                    TotalRcv = "%.2f MB" % self.devUtil._device.div(TotalRcv, 1024 * 1024, 2)
                elif TotalRcv > 1000:
                    TotalRcv ="%.2f KB" %  self.devUtil._device.div(TotalRcv, 1024, 2)
                else:
                    TotalRcv = '%d B' % TotalRcv
                if TotalSnd > 1000 * 1000 * 1000:
                    TotalSnd ="%.2f GB" %  self.devUtil._device.div(TotalSnd, 1024 * 1024 * 1024, 2)
                elif TotalSnd > 1000 * 1000:
                    TotalSnd = "%.2f MB" % self.devUtil._device.div(TotalSnd, 1024 * 1024, 2)
                elif TotalSnd > 1000:
                    TotalSnd ="%.2f KB" %  self.devUtil._device.div(TotalSnd, 1024, 2)
                else:
                    TotalSnd = '%d B' % TotalSnd
                self.socketio.emit('server_response',{ 'category':5, 'TotalRcv':TotalRcv, 'TotalSnd':TotalSnd, 'down': downloadSpeed,'up': uploadSpeed,'time': int(round(time.time() * 1000))},
                              namespace='/showPage')
            else:
                if count < 0:
                    print ('NET_thread exit')
                    break
                count -= 1
        print("T_NET_thread Exit")
