#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   OtherInfo.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/14 10:59   Zorfree      1.0         None
'''
from flask import  current_app
from _socket import gethostname

def getPersonID():
    try:
        return gethostname()
    except:
        return None


def paramToNumber(param):
    if param is None:
        return None
    paramStr, paramUnit = param.split(" ")
    if paramUnit == "B":
        paramNum = float(paramStr)
    elif paramUnit == "KB":
        paramNum = float(paramStr) * 1000
    elif paramUnit == "MB":
        paramNum = float(paramStr) * 1000 * 1000
    elif paramUnit == "GB":
        paramNum = float(paramStr) * 1000 * 1000 * 1000
    else:
        return None
    return paramNum

def timeInterval(start,end):
    if start is None or end is None:
        return None
    print(end,start)
    tmp = int(end) - (int(start) / 1000)
    if tmp < 60:
        return "%d s" % tmp
    elif tmp < 3600:
        return "%.2f m" % (tmp / 60)
    elif tmp < 216000:
        return "%.2f h" % (tmp / 3600)


def judgeRange(num):
    themeMap = {-2:["","red","很差"],-1:["layui-bg-orange","darkorange","较差"],
                0:["layui-bg-green","green","良好"],1:["layui-bg-green","green","较好"],2:["layui-bg-green","green","很好"]}
    if num < 0:
        if num < -0.15:
            return themeMap[-2]
        else:
            return themeMap[-1]
    elif num == 0:
        return themeMap[0]
    else:
        if num > 0.15:
            return themeMap[2]
        else:
            return themeMap[1]


def getEvaluation(CPUAverageRange,CPUMaxRange,PSSAverageRange,PSSMaxRange):
    evaScore = {}
    # evaDetail = {}
    if CPUAverageRange:
        evaScore["CPU均值"] =judgeRange(CPUAverageRange)
        # evaDetail["CPUAverage"] = evaDetail(CPUAverageRange)
    if CPUMaxRange:
        evaScore["CPU峰值"] = judgeRange(CPUMaxRange)
        # evaDetail["CPUMax"] = evaDetail(CPUMaxRange)
    if PSSAverageRange:
        evaScore["内存均值"] = judgeRange(PSSAverageRange)
        # evaDetail["PSSAverage"] = evaDetail(PSSAverageRange)
    if PSSMaxRange:
        evaScore["内存峰值"] = judgeRange(PSSMaxRange)
        # evaDetail["PSSMax"] = evaDetail(PSSMaxRange)
    return evaScore

def evaDetail():
    return None

def calcScore(CPUAverage,CPUMax,PSSAverage,PSSMax,downT,upT,readT,writeT):

    CPUAverageRange,CPUMaxRange,PSSAverageRange, PSSMaxRange = None, None, None, None
    QA_SCORE = current_app.config['QA_SCORE']
    QA_CPUAverage = current_app.config['QA_CPUAVERAGE']
    QA_CPUMax = current_app.config['QA_CPUMAX']
    QA_PSSAverage = current_app.config['QA_PSSAVERAGE']
    QA_PSSMax = current_app.config['QA_PSSMAX']

    CPUAVERAGE_PERCENT = current_app.config['CPUAVERAGE_PERCENT']
    CPUMAX_PERCENT = current_app.config['CPUMAX_PERCENT']
    PSSAVERAGE_PERCENT = current_app.config['PSSAVERAGE_PERCENT']
    PSSMAX_PERCENT = current_app.config['PSSMAX_PERCENT']
    # DOWNT_PERCENT = current_app.config['DOWNT_PERCENT']
    # UPT_PERCENT = current_app.config['UPT_PERCENT']
    # READT_PERCENT = current_app.config['READT_PERCENT']
    # WRITET_PERCENT = current_app.config['WRITET_PERCENT']
    if CPUAverage:
        CPUAverageRange = (QA_CPUAverage - CPUAverage) / QA_CPUAverage
    if CPUMax:
        CPUMaxRange = (QA_CPUMax - CPUMax) / QA_CPUMax
    if PSSAverage:
        PSSAverageRange = (QA_PSSAverage - PSSAverage) / QA_PSSAverage
    if PSSMax:
        PSSMaxRange = (QA_PSSMax - PSSMax) / QA_PSSMax
    reportEvaluation = getEvaluation(CPUAverageRange,CPUMaxRange,PSSAverageRange,PSSMaxRange)

    CPUAverageScore = int(CPUAverageRange * CPUAVERAGE_PERCENT)
    CPUMaxScore = int(CPUMaxRange * CPUMAX_PERCENT)
    PSSAverageScore = int(PSSAverageRange * PSSAVERAGE_PERCENT)
    PSSMaxScore = int(PSSMaxRange * PSSMAX_PERCENT)
    totalScore = CPUAverageScore + CPUMaxScore + PSSAverageScore + PSSMaxScore + QA_SCORE

    return totalScore, reportEvaluation, CPUAverageScore, CPUMaxScore, PSSAverageScore, PSSMaxScore