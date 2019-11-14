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

from flask import render_template, request, Blueprint, send_from_directory, current_app
from androidpanel.extensions import socketio,proSchedu,schedu

socket_bp = Blueprint('socket', __name__)

@socketio.on('disconnect', namespace='/showPage')
def showPage_disconnect():
    print("showPage 断开")

@socketio.on('disconnect', namespace='/proPage')
def showPage_disconnect():
    print("proPage 断开")


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