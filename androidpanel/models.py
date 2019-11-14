#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 19:45   Zorfree      1.0         None
'''

# import lib
from androidpanel.extensions import db


class ScriptConfig(db.Model):
    __tablename__ = "scriptconfig"
    LAY_TABLE_INDEX = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    tempId = db.Column(db.Integer)
    time = db.Column(db.Integer)
    type = db.Column(db.String(32))

    def getconfig(self):
        return {"LAY_TABLE_INDEX":self.LAY_TABLE_INDEX,"name":self.name,"tempId":self.tempId,"time":self.time,"type":self.type}


class ReportsConfig(db.Model):
    __tablename__ = "reportsconfig"
    id = db.Column(db.Integer, primary_key=True)
    reportID = db.Column(db.Integer)
    reportTime = db.Column(db.String(32))
    reportsScore = db.Column(db.Integer)
    appVersion = db.Column(db.String(32))
    deviceModel = db.Column(db.String(68))
    measurementProgram = db.Column(db.String(68))
    measurementPerson = db.Column(db.String(32))
    CPUAverage = db.Column(db.Float)
    CPUMax = db.Column(db.Float)
    PSSAverage = db.Column(db.Float)
    PSSMax = db.Column(db.Float)
    downT = db.Column(db.Float)
    upT = db.Column(db.Float)
    readT = db.Column(db.Float)
    writeT = db.Column(db.Float)

    def getAllconfig(self):
        return {"reportID":self.reportID,"reportTime":self.reportTime,"reportsScore":self.reportsScore,"appVersion":self.appVersion,"deviceModel":self.deviceModel
                ,"measurementProgram":self.measurementProgram,"measurementPerson":self.measurementPerson,"CPUAverage":self.CPUAverage,"CPUMax":self.CPUMax
                   ,"PSSAverage":self.PSSAverage,"PSSMax":self.PSSMax,"downT":self.downT,"upT":self.upT,"readT":self.readT,"writeT":self.writeT}
    def getSimpleconfig(self):
        return {"reportID":self.reportID,"reportTime":self.reportTime,"reportsScore":self.reportsScore,"deviceModel":self.deviceModel}