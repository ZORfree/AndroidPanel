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

from _socket import gethostname

def getPersonID():
    try:
        return gethostname()
    except:
        return None
