#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Mythread.py    
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/12 15:41   gxrao      1.0         None
'''
from threading import Thread,Event

class MyThread(Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__()
        self.__flag = Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False

 
