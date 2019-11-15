#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_OtherInfo.py    
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/14 11:06   Zorfree      1.0         None
'''


from androidpanel.utils.OtherInfo import getPersonID,judgeRange


# print(getPersonID())

for i in [0.6647058823529413,
0.8648,
-0.2467741935483871,
0.08423529411764706]:
    print(judgeRange(i))