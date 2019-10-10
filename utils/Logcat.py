#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Logcat.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/12 10:09   gxrao      1.0         None
'''
import time
import os
from subprocess import Popen,PIPE,STDOUT
import signal
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
# from utils.Mythread import MyThread
import inspect
import ctypes

class LOGCAT(object):

    def __init__(self):
        self._logpid = None
        self.logcount = 1
        self._scheduler = None
        self._handle = None
        self.t1=Thread(target=self.threadlog,daemon=True)
        self.logfile = None


    def threadlog(self):
        self.logfile = open('logcat.log', 'ab')
        self._handle = Popen(['adb', 'logcat', '-v', 'time', '*:D'], stdout=PIPE, stderr=STDOUT, bufsize=1)
        for line in self._handle.stdout:
            self.logfile.write(line)

    def getlog(self):
        print("执行了getlog")
        if self._handle != None:
            print("已在运行")
            self.stoplog()
        self._isendthread = False
        self.t1.start()
        # logshell = "adb logcat -v time > %s\logcat-%d.log"  %(os.getcwd(),self.logcount)
        # handle = subprocess.Popen(logshell, shell=True)
        # self._logpid = str(handle.pid)
        # self._handle = handle

    def stoplog(self,increase=False):
        print("执行了stoplog")
        if increase:
            self.logcount += 1
        # self._isendthread = True
        self.stop_thread(self.t1)
        self._handle.kill()
        # subprocess.Popen("taskkill /F /PID " + self._logpid, shell=True)
        # Popen("taskkill /F /T /PID %d" % self._handle.pid).kill()
        # os.kill(0, signal.CTRL_C_EVENT)
        # time.sleep(2)

        self._handle = None
        # self._logpid = None

    def start(self):
        self.getlog()
        self._scheduler = scheduler.add_job(self.getlog, 'interval', seconds=10)
        scheduler.start()

    def pause(self):
        self.stop()
        self._scheduler.pause()

    def resume(self):
        self.getlog()
        self._scheduler.resume()

    def shutdown(self):
        if self._scheduler != None:
            self._scheduler.remove()
        scheduler.shutdown(wait=False)








