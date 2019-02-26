#!/usr/bin/env python
# -*- coding:utf-8 -*-
#尝试获取，展现特定比赛场次的运动员运动轨迹。
#Robin  2017.2
# =============================================================
"""
Track NBA players' movement
"""
#版本兼容
from __future__ import absolute_import
from __future__ import division
#解析命令行参数
import argparse
import sys
#解压缩
import py7zlib
#统计分析
import pandas as pd
import numpy as np
#绘图
import matplotlib.pyplot as plt
#import seaborn as sns
import json
from Event3D import Event


def readlog(path):

    with open(path, 'rb') as fp:
        archive = py7zlib.Archive7z(fp)
        for name in archive.getnames():
            print(name)
            log = archive.getmember(name).read()
    return log


if __name__ == '__main__':
    log = readlog("data/2016NBASportVU/01.01.2016.DAL.at.MIA.7z")
    #将json转为Python格式
    logpy = json.loads(log)

    print 'Target: ',logpy.keys(),'\n'

    #读取特定events
    for _ in [15]:
        target_event = Event(logpy["events"][_])
        target_event.showMoments()

        print 'event_id: ',logpy["events"][_]["eventId"],'\n'
        #for i in range(len(logpy['events'][_]["moments"])):


    #print json.dumps(logpy, indent=4, sort_keys=True)

    # data_frame = pd.read_json(log)
    # print data_frame
