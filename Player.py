# -*- coding:utf-8 -*-
from Team import Team
class Player:
    #Player Definition by player movement info
    #Just player's number and position
    #
    def __init__(self,player):
        self.team = Team(player[0])
        self.id = player[1]
        self.x = player[2]
        self.y = player[3]
        self.z = 0.8
        self.color = self.team.color