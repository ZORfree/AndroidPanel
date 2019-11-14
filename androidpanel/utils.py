#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py    
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 20:04   Zorfree      1.0         None
'''
 
deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)
device = APPTool(adb)
devUtil = devUtils(device)
proUtil = proUtils(device)
script = SCRIPT(adb)

proUtil.setPackageName('com.iflytek.xiri')
proSchedu = ProSchedu(adb, proUtil, socketio)
schedu = Schedu(adb, devUtil, socketio)
