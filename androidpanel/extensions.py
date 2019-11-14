#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   socket.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 20:01   Zorfree      1.0         None
'''
from flask_socketio import SocketIO
import os
from flask_sqlalchemy import SQLAlchemy
from androidpanel.utils.Commands import AndroidCommands
from androidpanel.utils.AppTool import APPTool
from androidpanel.utils.DeviceUtils import devUtils
from androidpanel.utils.ProcessUtils import proUtils
from androidpanel.schedu.Script import SCRIPT


socketio = SocketIO()
db = SQLAlchemy()
deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)
device = APPTool(adb)
devUtil = devUtils(device)
proUtil = proUtils(device)
script = SCRIPT(adb)

proUtil.setPackageName('com.iflytek.xiri')

from androidpanel.schedu.ProcessSchedu import ProSchedu
from androidpanel.schedu.Schedu import Schedu

proSchedu = ProSchedu(adb, proUtil, socketio)
schedu = Schedu(adb, devUtil, socketio)






