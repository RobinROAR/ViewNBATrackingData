# -*- coding:utf-8 -*-
class Ball:
    '''Ball Definition by ball movement info'''
    def __init__(self,ball):
        self.x = ball[2]
        self.y = ball[3]
        self.z = ball[4]/5
        self.radius = ball[4]
        self.color = '#ff8c00'

