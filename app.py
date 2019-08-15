# coding=utf-8
from flask import Flask, url_for,render_template
from flask_socketio import send, emit,SocketIO,SocketIOTestClient
import time
import datetime
from utils.Commands import AndroidCommands
from utils.AppTool import APPTool
from utils.deviceUtils import devUtils
import os
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from threading import Lock

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
threadCPU ,threadRAM , threadFPS, threadDISK, threadIO, threadNET= None ,None, None, None, None, None

# thread_lock = Lock()
deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)
device = APPTool(adb)
devUtil = devUtils(device)
retryTimes = 6
# 后台线程 产生数据，即刻推送至前端
def CPU_thread():
    count = retryTimes
    while adb.enabled:
        cpuUsage = devUtil.cpuUsage()
        if cpuUsage:
            socketio.emit('server_response',{ 'category':1,'data': '%.2f' %cpuUsage},
                          namespace='/showPage')
            socketio.sleep(1)
        else:
            if count < 0:
                print 'CPU_thread exit'
                break
            count -= 1
def RAM_thread():
    count = retryTimes
    while adb.enabled:
        MemTotal, Memfree, MemUsage = devUtil.ramUsage()
        if MemUsage:
            socketio.emit('server_response',{ 'category':2,'total': MemTotal,'free':Memfree,'usage':MemUsage},
                          namespace='/showPage')
            socketio.sleep(1)
        else:
            if count < 0:
                print 'RAM_thread exit'
                break
            count -= 1
def FPS_thread():
    while adb.enabled:
        fps_List = []
        for i in range(15):
            try:
                fps = devUtil.FPSData()
            except Exception as e:
                print e
                continue
            if fps:
                fps_List.append(fps)
        if fps_List:
            FPS = devUtil._device.div(sum(fps_List), len(fps_List),1)
            cent = devUtil._device.div(FPS,60,2) * 100
            socketio.emit('server_response',{ 'category':3,'value':FPS, 'cent':cent},
                          namespace='/showPage')
def DISK_thread():
    count = retryTimes
    while adb.enabled:
        totalRom, usedRom, freeRom, romUsage = devUtil.diskUsage()
        # romUsage = devUtil.diskUsage()
        if romUsage:
            socketio.emit('server_response',{ 'category':4,'text': str(usedRom)+"/"+str(totalRom)+'G','value':romUsage},
                          namespace='/showPage')
            # socketio.emit('server_response',{'category': 4, 'value': romUsage})
            socketio.sleep(5)
        else:
            if count < 0:
                print 'DISK_thread exit'
                break
            count -= 1
def IO_thread():
    count = retryTimes
    while adb.enabled:
        readSpeed, writeSpeed, totalReadKb, totalWriteKb = devUtil.ioSpeed()
        socketio.sleep(1)
        if readSpeed or writeSpeed or totalReadKb or totalWriteKb:
            if totalReadKb > 1000 * 1000:
                totalReadKb = "%.2f GB" % devUtil._device.div(totalReadKb, 1024 * 1024, 2)
            elif totalReadKb > 1000:
                totalReadKb ="%.2f MB" %  devUtil._device.div(totalReadKb, 1024, 2)
            else:
                totalReadKb = '%d KB' % totalReadKb
            if totalWriteKb > 1000 * 1000:
                totalWriteKb = "%.2f GB" % devUtil._device.div(totalWriteKb, 1024 * 1024, 2)
            elif totalWriteKb > 1000:
                totalWriteKb ="%.2f MB" %  devUtil._device.div(totalWriteKb, 1024, 2)
            else:
                totalWriteKb = '%d KB' % totalWriteKb
            socketio.emit('server_response',{ 'category':6, 'totalRead':totalReadKb, 'totalWrite':totalWriteKb, 'read': readSpeed,'write': writeSpeed,'time': int(round(time.time() * 1000))},
                          namespace='/showPage')
        else:
            if count < 0:
                print 'IO_thread exit'
                break
            count -= 1
def NET_thread():
    count = retryTimes
    while adb.enabled:
        try:
            uploadSpeed, downloadSpeed, TotalRcv, TotalSnd = devUtil.netSpeed()
        except Exception as e:
            print e
            continue
        socketio.sleep(1)
        if uploadSpeed or downloadSpeed or TotalRcv or TotalSnd:
            if TotalRcv > 1000 * 1000 * 1000:
                TotalRcv ="%.2f GB" %  devUtil._device.div(TotalRcv, 1024 * 1024 * 1024, 2)
            elif TotalRcv > 1000 * 1000:
                TotalRcv = "%.2f MB" % devUtil._device.div(TotalRcv, 1024 * 1024, 2)
            elif TotalRcv > 1000:
                TotalRcv ="%.2f KB" %  devUtil._device.div(TotalRcv, 1024, 2)
            else:
                TotalRcv = '%d B' % TotalRcv
            if TotalSnd > 1000 * 1000 * 1000:
                TotalSnd ="%.2f GB" %  devUtil._device.div(TotalSnd, 1024 * 1024 * 1024, 2)
            elif TotalSnd > 1000 * 1000:
                TotalSnd = "%.2f MB" % devUtil._device.div(TotalSnd, 1024 * 1024, 2)
            elif TotalSnd > 1000:
                TotalSnd ="%.2f KB" %  devUtil._device.div(TotalSnd, 1024, 2)
            else:
                TotalSnd = '%d B' % TotalSnd
            socketio.emit('server_response',{ 'category':5, 'TotalRcv':TotalRcv, 'TotalSnd':TotalSnd, 'down': downloadSpeed,'up': uploadSpeed,'time': int(round(time.time() * 1000))},
                          namespace='/showPage')
        else:
            if count < 0:
                print 'NET_thread exit'
                break
            count -= 1
showPage = False
ProcessesPage = False

@app.route('/')
def Dashboard():
    showPage = True
    ProcessesPage = False
    devInfoList = devUtil.devInfo()
    return render_template("index.html", async_mode=socketio.async_mode,page="Dashboard",hostname="B860AV1.1-T",running="22小时20分钟",devInfo = devInfoList)

@app.route('/Processes')
def Processes():
    showPage = False
    ProcessesPage = True
    return render_template("index.html", page="Processes",hostname="B860AV1.1-T",running="22小时20分钟")



@socketio.on('connect',namespace="/showPage")
def connected_msg():
    global threadCPU, threadRAM, threadFPS, threadDISK, threadIO, threadNET
    if threadCPU is None:
        threadCPU = socketio.start_background_task(target=CPU_thread)
    if threadRAM is None:
        threadRAM = socketio.start_background_task(target=RAM_thread)
    if threadFPS is None:
        threadFPS = socketio.start_background_task(target=FPS_thread)
    if threadDISK is None:
        threadDISK = socketio.start_background_task(target=DISK_thread)
    if threadIO is None:
        threadIO = socketio.start_background_task(target=IO_thread)
    if threadNET is None:
        threadNET = socketio.start_background_task(target=NET_thread)


if __name__ == '__main__':

    socketio.run(app)
