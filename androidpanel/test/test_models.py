#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_models.py    
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/14 13:57   Zorfree      1.0         None
'''
 
from androidpanel.extensions import db
from androidpanel.models import ScriptConfig,ReportsConfig

def fake_ScriptConfig():
    testscript = [{'LAY_TABLE_INDEX': 0, 'name': '请填写名称', 'tempId': 1569466124400, 'time': '1', 'type': '6'}]
    scriptconfig = ScriptConfig(
        name='请填写名称',
        tempId=1569466124400,
        time='1',
        type='6'
    )
    db.session.add(scriptconfig)
    db.session.commit()


session = db.session()
scriptData = session.query(ScriptConfig).all()
for i in scriptData:
    print(i)

