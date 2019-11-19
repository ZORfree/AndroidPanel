#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   OtherInfo.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 19:45   Zorfree      1.0         None
'''
from flask import render_template, request, Blueprint
import time,os
from datetime import datetime
from androidpanel.extensions import script,adb,devUtil,db,device
from androidpanel.models import ScriptConfig, ReportsConfig
from androidpanel.utils.OtherInfo import getPersonID,paramToNumber,calcScore, timeInterval, getTempData
main_bp = Blueprint('main', __name__)

from androidpanel.extensions import socketio,proSchedu,schedu

@main_bp.route('/')
def Dashboard():
    adb.showPage = True
    adb.proPage = False
    adb.scriptPage = False
    refreshPage()
    devInfoList = devUtil.devInfo()
    return render_template("main/index.html", async_mode=socketio.async_mode,devInfo = devInfoList)

@main_bp.route('/Processes')
def Processes():
    adb.showPage = False
    adb.proPage = True
    adb.scriptPage = False
    refreshPage()
    return render_template("main/process.html", async_mode=socketio.async_mode)

@main_bp.route('/Script')
def Script():
    adb.showPage = False
    adb.proPage = False
    adb.scriptPage = True
    refreshPage()
    return render_template("main/scriptproject.html",data=getMeasurementProgram())

@main_bp.route('/Report')
def Report_Items():
    adb.showPage = False
    adb.proPage = False
    adb.scriptPage = False
    refreshPage()

    if os.path.exists("data.db"):
        reports =[i.getSimpleconfig() for i in ReportsConfig.query.all()]
        print(reports)

    return render_template("main/report.html",switch=False,reports=reports)

@main_bp.route('/saveScript',methods=['POST'])
def Save():
    for i in request.form:
        dataList = eval(i)
        break

    scriptList = []
    TIME  = int(time.time())
    for i in dataList:
        print(i)
        invTime = int(i["time"])
        type = i["type"]
        if type == "1":
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
            scriptdict["fun"] = typeToInfo(type)[0]
            scriptdict["inv"] = typeToInfo(type)[1]
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

    session = db.session()
    session.query(ScriptConfig).delete()
    for i in dataList:
        configlist = ScriptConfig(
            LAY_TABLE_INDEX=i['LAY_TABLE_INDEX'],
            name=i['name'],
            tempId=i['tempId'],
            time=i['time'],
            type=i['type']
        )
        session.add(configlist)
    session.commit()
    return 'success'

@main_bp.route('/Upload',methods=['POST'])
def Upload():
    tempData = getTempData()
    timestamp = int(time.time())
    reportTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))

    deviceModel = ""
    devInfoList = devUtil.devInfo()
    if devInfoList[0]:
        deviceModel = deviceModel + devInfoList[0]
    if devInfoList[1]:
        deviceModel = deviceModel + devInfoList[1]

    PSSAverage = paramToNumber(request.form.get("PSSAverage"))
    PSSMax = paramToNumber(request.form.get("PSSMax"))
    CPUAverage = request.form.get("CPUAverage")
    spendTime = timeInterval(request.form.get("startTime"),timestamp)
    if CPUAverage:
        CPUAverage = float(CPUAverage.split(" ")[0])
    CPUMax = request.form.get("CPUMax")
    if CPUMax:
        CPUMax = float(CPUMax.split(" ")[0])
    upT = paramToNumber(request.form.get("upT"))
    readT = paramToNumber(request.form.get("readT"))
    writeT = paramToNumber(request.form.get("writeT"))
    downT = paramToNumber(request.form.get("downT"))
    appVersion = device.getAppVersion("com.iflytek.xiri")
    measurementProgram = ""
    measurementProgramList = getMeasurementProgram()
    if measurementProgramList:
        for i in measurementProgramList:
            measurementProgram  = measurementProgram + typeToInfo(i["type"])[2] + i["time"]
    session = db.session()
    reportScore, reportEvaluation, CPUAverageScore, CPUMaxScore, PSSAverageScore, PSSMaxScore = calcScore(CPUAverage,CPUMax,PSSAverage,PSSMax,downT,upT,readT,writeT)
    reportsconfig =ReportsConfig(
        reportScore = reportScore,
        reportEvaluation = reportEvaluation,
        CPUAverageScore = CPUAverageScore,
        CPUMaxScore = CPUMaxScore,
        PSSAverageScore = PSSAverageScore,
        PSSMaxScore = PSSMaxScore,
        appVersion = appVersion,
        deviceModel = deviceModel,
        measurementProgram = measurementProgram,
        measurementPerson = getPersonID(),
        CPUData = tempData.get("CPU"),
        PSSData = tempData.get("PSS"),
        NETData = tempData.get("NET"),
        IOData = tempData.get("IO"),
        reportID = timestamp,
        reportTime = reportTime,
        spendTime = spendTime,
        CPUAverage = CPUAverage,
        CPUMax = CPUMax,
        PSSAverage = PSSAverage,
        PSSMax=PSSMax,
        downT = downT,
        upT = upT,
        readT = readT,
        writeT = writeT
                      )
    session.add(reportsconfig)
    session.commit()
    return 'success'



@main_bp.route('/reports/<int:time>/')
def Report_Detail(time):
    print(time)
    if os.path.exists("data.db"):
        report = ReportsConfig.query.filter(ReportsConfig.reportID == time).first().getAllconfig()
        print(report)
    return render_template("report/reportdetailv2.html",report=report)


@main_bp.route('/reports/<string:time>/<string:type>')
def Report_get_data(time,type):
    print(time)
    if os.path.exists("data.db"):
        report = ReportsConfig.query.filter(ReportsConfig.reportID == time).first().getData(type)
        print(report)
    return str(report)


@main_bp.route('/Switch/<int:switch>')
def Switch(switch):
    if adb.showPage:
        if switch:
            if schedu.state() == 1:
                schedu.pause()
        else:
            schedu.resume()
    elif adb.proPage:
        if switch:
            if proSchedu.state() == 1:
                proSchedu.pause()
        else:
            proSchedu.resume()
    else:
        if switch:
            if script.state() == 1:
                script.pause()
        else:
            script.resume()
    return {"code":True},200

@main_bp.route('/getSwitch')
def getSwitch():
    if adb.showPage:
        print("getSwitch %d" % schedu.state())
        if schedu.state() == 1:
            return {"code":True}
        return  {"code":False}
    elif adb.proPage:
        print("getSwitch %d" % proSchedu.state())
        if proSchedu.state() == 1:
            return {"code": True}
        return {"code": False}
    else:
        print("getSwitch %d" % script.state())
        if script.state() == 1:
            return {"code": True}
        return {"code": False}

def refreshPage():
    if adb.showPage:
        if proSchedu.state() == 1:
            proSchedu.pause()
            print("暂停进程任务")
    elif adb.proPage:
        print("进程页")
        if schedu.state() == 1:
            schedu.pause()
            print("暂停整机任务")
    else:
        if proSchedu.state() == 1:
            proSchedu.pause()
            print("暂停进程任务")
        if schedu.state() == 1:
            schedu.pause()
            print("暂停整机任务")



def getMeasurementProgram():
    scriptData = None
    if os.path.exists("data.db"):
        scriptData =[i.getconfig() for i in ScriptConfig.query.all()]
        print(scriptData)
    return scriptData

def typeToInfo(type):
    typeFunMap = {"1":[script.H5,15,"H5、直、点、回、技能"],"2":[script.H5,15,"H5"],"3":[script.Live,15,"直播"],"4":[script.Vod,6,"点播"],"5":[script.Playback,5,"回看"],"6":[script.Skill,6,"技能"]}
    return typeFunMap[str(type)]


