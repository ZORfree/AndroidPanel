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
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
import time
class Schedu(object):
    def __init__(self, adb,devUtil,socketio):
        self.adb = adb
        self.devUtil = devUtil
        self.socketio = socketio
        self.retryTimesCPU = 6
        self.retryTimesRAM = 6
        self.retryTimesFPS = 6
        self.retryTimesDISK = 6
        self.retryTimesNET = 6
        self.retryTimesIO = 6

    def Start(self):
        self.CPU = scheduler.add_job(self.CPU_thread, 'interval', seconds=2)
        self.RAM = scheduler.add_job(self.RAM_thread, 'interval', seconds=2)
        self.FPS = scheduler.add_job(self.FPS_thread, 'interval', seconds=2)
        self.DISK = scheduler.add_job(self.DISK_thread, 'interval', seconds=5)
        self.NET = scheduler.add_job(self.NET_thread, 'interval', seconds=1)
        self.IO = scheduler.add_job(self.IO_thread, 'interval', seconds=1)
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
        if  self.adb.enabled:
            cpuUsage =  self.devUtil.cpuUsage()
            if cpuUsage:
                self.socketio.emit('server_response',{ 'category':1,'data': '%.2f' %cpuUsage},
                              namespace='/showPage')
                self.socketio.sleep(1)
            else:
                if self.retryTimesCPU < 0:
                    print("T_CPU_thread Exit")
                    self.CPU.remove()
                self.retryTimesCPU -= 1


    def RAM_thread(self):
        if self.adb.enabled:
            MemTotal, Memfree, MemUsage = self.devUtil.ramUsage()
            if MemUsage:
                self.socketio.emit('server_response',{ 'category':2,'total': MemTotal,'free':Memfree,'usage':MemUsage},
                              namespace='/showPage')
                self.socketio.sleep(1)
            else:
                if self.retryTimesRAM < 0:
                    print("T_RAM_thread Exit")
                    self.RAM.remove()
                self.retryTimesRAM -= 1


    def FPS_thread(self):
        if self.adb.enabled:
            fps_List = []
            for i in range(15):
                try:
                    fps = self.devUtil.FPSData()
                except Exception as e:
                    print (e)
                    if self.retryTimesFPS < 0:
                        print("T_FPS_thread Exit")
                        self.FPS.remove()
                    self.retryTimesFPS -= 1
                if fps:
                    fps_List.append(fps)
            if fps_List:
                FPS = self.devUtil._device.div(sum(fps_List), len(fps_List),1)
                cent = self.devUtil._device.div(FPS,60,2) * 100
                self.socketio.emit('server_response',{ 'category':3,'value':FPS, 'cent':cent},
                              namespace='/showPage')


    def DISK_thread(self):
        if self.adb.enabled:
            totalRom, usedRom, freeRom, romUsage = self.devUtil.diskUsage()
            if romUsage:
                self.socketio.emit('server_response',{ 'category':4,'text': str(usedRom)+"/"+str(totalRom)+'G','value':romUsage},
                              namespace='/showPage')
            else:
                if self.retryTimesDISK < 0:
                    self.DISK.remove()
                    print("T_DISK_thread Exit")
                self.retryTimesDISK -= 1


    def IO_thread(self):
        if self.adb.enabled:
            readSpeed, writeSpeed, totalReadKb, totalWriteKb = self.devUtil.ioSpeed()
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
                if self.retryTimesIO < 0:
                    self.IO.remove()
                    print("T_IO_thread Exit")
                self.retryTimesIO -= 1


    def NET_thread(self):
        if self.adb.enabled:
            uploadSpeed, downloadSpeed, TotalRcv, TotalSnd = self.devUtil.netSpeed()
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
                if self.retryTimesNET < 0:
                    self.NET.remove()
                    print("T_NET_thread Exit")
                self.retryTimesNET -= 1

