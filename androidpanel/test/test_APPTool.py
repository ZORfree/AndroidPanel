#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_APPTool.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/14 10:35   Zorfree      1.0         None
'''
 
from androidpanel.utils.Commands import AndroidCommands
from androidpanel.utils.AppTool import APPTool
import os
deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)

apptool = APPTool(adb)

print(apptool.getVersion("com.iflytek.xiri2.hal"))
