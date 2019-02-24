# -*- coding:utf-8 -*-
from Ball import Ball
from Player import Player
class Moment:
    '''Moment defination by givging moment json'''
    '''抽象化原始json信息，将ball和player信息分离'''
    def __init__(self,moment):
        self.quarter = moment[0]
        self.game_clock = moment[2]
        self.shot_clock = moment[3]
        ball = moment[5][0]
        self.ball = Ball(ball)
        #只是当前moment出现过的球员
        players = moment[5][1:]
        self.players = [ Player(player) for player in players]
