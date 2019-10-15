#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Script.py    
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/23 9:29   gxrao      1.0         None
'''
import time
import random
from datetime import datetime
import os
from utils.Commands import AndroidCommands
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
class SCRIPT(object):

    def __init__(self,adb):
        self._adb = adb
        self._liveList = ["安徽卫视","cctv-1","江西卫视"]
        self._playbackList = ["安徽卫视的节目单","中央一套的节目单","四川卫视的节目单"]
        self._vodList = ["周星驰的电影","刘德华的电影","成龙的电影"]
        self._skillList = ["合肥的天气", "科大讯飞的股票", "给我讲个笑话"]
        self.baseCmd = "am startservice -a com.iflytek.xiri2.START --es startmode text --es text "

    def Add_Job(self,jobs):
        names = locals()
        # index = 0
        for job in jobs:
            if  "run_date" in job:
                scheduler.add_job(job["fun"], 'date', run_date=job["run_date"],args=job["arg"])
            else:
                scheduler.add_job(job["fun"], 'interval', seconds=job["inv"], start_date=job["start_date"],
                                  end_date=job["end_date"])
            # names['job%d' % index] = scheduler.add_job(job["fun"], 'interval', seconds=job["inv"], start_date=job["start_date"], end_date=job["end_date"])

    def Start(self):
        scheduler.start()
    # keyevent 4 返回 3 主页 19 上 20 下  21 左 22 右  23 确定  92 上一页  93 下一页
    def Keydown(self,keyevent):
        self._adb.RunShellCommandNoResult('input keyevent %d' % keyevent)
        # self._adb.ospopen('input keyevent %d' %keyevent)
        # self._adb.RunShellCommand('input keyevent %d' %keyevent,False)
        # os.popen('adb shell input keyevent %d' %keyevent)
    def Live(self):
        #间隔8s
        print("Live")
        self._adb.RunShellCommandNoResult(self.baseCmd + random.choice(self._liveList))
        # self._adb.ospopen(self.baseCmd + "中央一套")
        # self._adb.RunShellCommand(self.baseCmd + "中央一套",False)
        # time.sleep(8)

    def Vod(self):
        #间隔5s以上
        print("Vod")
        # self.Keydown(3)
        # time.sleep(1)
        self._adb.RunShellCommandNoResult(self.baseCmd + random.choice(self._vodList))
        # self._adb.ospopen(self.baseCmd + "周星驰的电影")
        # self._adb.RunShellCommand(self.baseCmd + "周星驰的电影",False)
        # os.popen(self.baseCmd + "周星驰的电影")


    def Playback(self):
        #间隔5s
        print("Playback")
        self._adb.RunShellCommandNoResult(self.baseCmd + random.choice(self._playbackList))
        # self._adb.ospopen(self.baseCmd + "回看中央一套")
        # self._adb.RunShellCommand(self.baseCmd + "回看中央一套",False)
        # time.sleep(1)


    def H5(self):
        print("H5")
        self.Keydown(3)
        self._adb.RunShellCommandNoResult(self.baseCmd + "语音专区")
        # self._adb.ospopen(self.baseCmd + "语音专区")
        # self._adb.RunShellCommand(self.baseCmd + "语音专区",False)
        # time.sleep(2)

    def Skill(self):
        #间隔5s
        print("Skill")
        self.Keydown(4)
        # time.sleep(1)
        self._adb.RunShellCommandNoResult(self.baseCmd + random.choice(self._skillList))
        # self._adb.ospopen(self.baseCmd + "今日天气")
        # self._adb.RunShellCommand(self.baseCmd + "今日天气",False)
        # os.popen(self.baseCmd + "今日天气")

    def removejobs(self):
        print("removejobs")
        for i in scheduler.get_jobs():
            i.remove()
            print("移除一个JOB：" + i.name)
    def state(self):
        #未初始化0，进行中1，暂停2
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
        try:
            scheduler.resume()
        except Exception as e:
            print(e)

 
