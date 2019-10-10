# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request
from flask_socketio import send, emit,SocketIO,SocketIOTestClient
from sqlitedict import SqliteDict
import time
from datetime import datetime
from utils.ProcessThread import ProThread
from utils.Commands import AndroidCommands
from utils.AppTool import APPTool
from utils.DeviceUtils import devUtils
from utils.ProcessUtils import proUtils
from utils.Thread import Thread
import os
import re
from utils.Script import SCRIPT
import sys
from threading import Lock

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode,ping_interval=2,ping_timeout=5)

# thread_lock = Lock()
deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)
device = APPTool(adb)
devUtil = devUtils(device)
proUtil = proUtils(device)
totalThread = Thread(adb,devUtil,socketio)
proThread = ProThread(adb,proUtil,socketio)
script = SCRIPT(adb)
from utils.ProcessSchedu import ProSchedu
from utils.Schedu import Schedu


proUtil.setPackageName('com.iflytek.xiri')
proSchedu = ProSchedu(adb, proUtil, socketio)
schedu = Schedu(adb, devUtil, socketio)
threadCPU ,threadRAM , threadFPS, threadDISK, threadIO, threadNET = None ,None, None, None, None, None
proThreadCPU, proThreadRAM, proThreadIO, proThreadNET = None, None, None, None

def refreshPage():
    if adb.showPage:
        if proSchedu.state() == 1:
            proSchedu.pause()
            print("暂停进程任务")
    elif adb.proPage:
        if schedu.state() == 1:
            schedu.pause()
            print("暂停整机任务")
    elif adb.scriptPage:
        if proSchedu.state() == 1:
            proSchedu.pause()
            print("暂停进程任务")
        if schedu.state() == 1:
            schedu.pause()
            print("暂停整机任务")


@app.route('/')
def Dashboard():
    adb.showPage = True
    adb.proPage = False
    adb.scriptPage = False
    refreshPage()
    devInfoList = devUtil.devInfo()
    return render_template("index.html", async_mode=socketio.async_mode,devInfo = devInfoList)

@app.route('/Processes')
def Processes():
    adb.showPage = False
    adb.proPage = True
    adb.scriptPage = False
    refreshPage()
    return render_template("process.html", async_mode=socketio.async_mode)

@app.route('/Script')
def Script():
    adb.showPage = False
    adb.proPage = False
    adb.scriptPage = True
    refreshPage()
    with SqliteDict('./data.db') as mydict:
        scriptData = mydict.get('script')
        print(scriptData)
    return render_template("scriptproject.html",data=scriptData)

@app.route('/SaveScript',methods=['POST'])
def Save():
    for i in request.form:
        dataList = eval(i)
        break
    typeFunMap = {"2":[script.H5,15],"3":[script.Live,15],"4":[script.Vod,6],"5":[script.Playback,5],"6":[script.Skill,6]}
    scriptList = []
    TIME  = int(time.time())
    for i in dataList:
        print(i)
        invTime = int(i["time"])
        if i["type"] == "1":
            defaultScriptList = [
                {"fun": script.Live, "inv": 15, "start_date": datetime.fromtimestamp(TIME),
                 "end_date": datetime.fromtimestamp(TIME + invTime * 60)},
                {"fun": script.Keydown,"run_date": datetime.fromtimestamp(TIME + invTime * 60 + 10),"arg":[3]},
                {"fun": script.Vod, "inv": 6, "start_date": datetime.fromtimestamp(TIME + invTime * 60 + 10 * 2),
                 "end_date": datetime.fromtimestamp(TIME + invTime * 60 * 2 + 10 * 2)},
                {"fun": script.Keydown,"run_date": datetime.fromtimestamp(TIME + invTime * 60 * 2 + 10 * 3),"arg":[3]},
                {"fun": script.Playback, "inv": 6, "start_date": datetime.fromtimestamp(TIME + invTime * 60 * 2 + 10 * 4),
                 "end_date": datetime.fromtimestamp(TIME + invTime * 60 * 3 + 10 * 4)},
                {"fun": script.Keydown,"run_date": datetime.fromtimestamp(TIME + invTime * 60 * 3 + 10 * 5),"arg":[3]},
                {"fun": script.Skill, "inv": 6, "start_date": datetime.fromtimestamp(TIME + invTime * 60 * 3 + 10 * 6),
                 "end_date": datetime.fromtimestamp(TIME + invTime * 60 * 4 + 10 * 6)},
                {"fun": script.Keydown,"run_date": datetime.fromtimestamp(TIME + invTime * 60 * 4 + 10 * 7),"arg":[3]}
            ]
            TIME = TIME + invTime * 60 * 4 + 10 * 8
            scriptList.extend(defaultScriptList)
        else:
            scriptdict = {}
            scriptdict["fun"] = typeFunMap[i["type"]][0]
            scriptdict["inv"] = typeFunMap[i["type"]][1]
            scriptdict["start_date"] = datetime.fromtimestamp(TIME)
            scriptdict["end_date"] = datetime.fromtimestamp(TIME + invTime * 60)
            scriptList.append(scriptdict)
            scriptList.append({"fun": script.Keydown,"run_date": datetime.fromtimestamp(TIME + invTime * 60 + 10),"arg":[3]})
            TIME = TIME + invTime* 60 + 10 * 2
    # scriptList.append({"fun": script.shutdown,"run_date": datetime.fromtimestamp(TIME + 5),"arg":[]})
    if script.state():
        print(script.state())
        script.removejobs()
        script.Add_Job(scriptList)
    else:
        if scriptList != None:
            script.Add_Job(scriptList)
            script.Start()
    with SqliteDict('./data.db') as mydict:
        mydict['script'] = dataList
        mydict.commit()
    return 'success'


@socketio.on('disconnect', namespace='/showPage')
def showPage_disconnect():
    print("showPage 断开")

@socketio.on('disconnect', namespace='/proPage')
def showPage_disconnect():
    print("proPage 断开")

# @socketio.on('connect',namespace="/showPage")
# def connected_msg():
#     print ('Already Connect')
#     global threadCPU, threadRAM, threadFPS, threadDISK, threadIO, threadNET
#     print(threadCPU, threadRAM, threadFPS, threadDISK, threadIO, threadNET)
#     if threadCPU is None:
#         threadCPU = socketio.start_background_task(target=totalThread.CPU_thread)
#     if threadRAM is None:
#         threadRAM = socketio.start_background_task(target=totalThread.RAM_thread)
#     if threadFPS is None:
#         threadFPS = socketio.start_background_task(target=totalThread.FPS_thread)
#     if threadDISK is None:
#         threadDISK = socketio.start_background_task(target=totalThread.DISK_thread)
#     if threadIO is None:
#         threadIO = socketio.start_background_task(target=totalThread.IO_thread)
#     if threadNET is None:
#         threadNET = socketio.start_background_task(target=totalThread.NET_thread)

@socketio.on('connect',namespace="/showPage")
def connected_msg():
    print ('Already Connect')
    scheduState = schedu.state()
    if scheduState == 0:
        schedu.Start()
    elif scheduState == 2:
        schedu.resume()
    print(schedu.state())

@socketio.on('connect',namespace="/proPage")
def connected_msg_pro():
    print('Process Connect')
    proScheduState = proSchedu.state()
    if proScheduState == 0:
        proSchedu.Start()
    elif proScheduState == 2:
        proSchedu.resume()
    print(proSchedu.state())

# @socketio.on('connect',namespace="/proPage")
# def connected_msg_pro():
#     print ('Process Connect')
#     proUtil.setPackageName('com.iflytek.xiri')
#     global proThreadCPU, proThreadRAM, proThreadIO, proThreadNET
#     if proThreadCPU is None:
#         proThreadCPU = socketio.start_background_task(target=proThread.CPU_thread)
#     if proThreadRAM is None:
#         proThreadRAM = socketio.start_background_task(target=proThread.RAM_thread)
#     if proThreadIO is None:
#         proThreadIO = socketio.start_background_task(target=proThread.IO_thread)
#     if proThreadNET is None:
#         proThreadNET = socketio.start_background_task(target=proThread.NET_thread)


if __name__ == '__main__':

    socketio.run(app)
