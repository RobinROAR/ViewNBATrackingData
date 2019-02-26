# -*- coding:utf-8 -*-
from Constant import Constant
from Moment import Moment
from Team import Team
#画图
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
#动画
from matplotlib import animation
from mpl_toolkits.mplot3d import proj3d
from matplotlib._png import read_png
#常用图形
from matplotlib.patches import Circle, Rectangle, Arc

class Event:
    '''
    Event definition and drawing by event json
    '''
    def __init__(self,event):
        '''
        :param event: event in list(events)
        '''
        #根据Json结构倒入moments
        moments = event["moments"]
        #self.moments is a list for moment instances
        self.moments = [Moment(moment) for moment in moments]
        #处理队员
        #handle all players
        players = event["visitor"]["players"] + event["home"]["players"]
        player_ids = [player["playerid"] for player in players]
        player_names = [" ".join([player["firstname"],player["lastname"]]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        #将球员信息组合成dict形式： {player_id: [ name, jersey]}, 定义成员变量
        #Compress player information in dict
        self.player_ids_dict = dict(zip(player_ids,zip(player_names,player_jerseys)))

    def update_radius(self, i, player_circles, ball_circle, annotations, clock_info,ax):
        '''
        用于更新当前时刻的位置
        :param i: index in moments
        :param player_circles: player
        :param ball_circle: ball
        :param annotations:
        :param clock_info: clock
        :return: updated player-circle and ball-circle
        '''
        moment = self.moments[i]
        for j, circle in enumerate(player_circles):
            #当前circle位置
            circle.set_data(moment.players[j].x, moment.players[j].y)
            circle.set_3d_properties(moment.players[j].z)

            #球员号码位置，与circle重叠
            x_, y_, _ = proj3d.proj_transform(moment.players[j].x, moment.players[j].y,moment.players[j].z, ax.get_proj())
            annotations[j].set_position((x_, y_))

            #clock
            clock_test = 'Quarter {:d}\n {:02d}:{:02d}\n {:03.1f}'.format(
                moment.quarter,
                int(moment.game_clock) % 3600 // 60,
                int(moment.game_clock) % 60,  moment.shot_clock)
            #update clock
            clock_info.set_text(clock_test)
        ball_circle.set_data(moment.ball.x, moment.ball.y)
        ball_circle.set_3d_properties(moment.ball.z)

        return player_circles, ball_circle,clock_info,annotations


    def showMoments(self):

        fig = plt.figure(figsize= (20,10))


        ax = fig.gca(projection = '3d')
        plt.subplots_adjust(bottom=0.2)

        #设置坐标轴，定位子图位置
        ax.set_xlim3d([Constant.X_MIN, Constant.X_MAX])
        ax.set_ylim3d([Constant.Y_MIN, Constant.Y_MAX])
        ax.set_zlim3d([0, 5])

        #ax为返回的axes instance，设置关闭坐标轴，关闭
        #ax.axis('off')
        ax.grid(False)


        #设置变量
        start_moment = self.moments[0]
        player_dict = self.player_ids_dict

        #显示时钟信息
        clock_info = ax.text2D(0.5,1, "", transform = ax.transAxes )
        #球员号码
        annotations = [ax.text2D(0,0,self.player_ids_dict[player.id][1], color = 'w', horizontalalignment = 'center', verticalalignment = 'center', fontweight = 'bold') for player in start_moment.players ]

        #排序moment内的球员，0-4为主队，5-9为客队
        sorted_player = sorted(start_moment.players, key = lambda player: player.team.id)

        #表格标签，颜色
        column_labels = [sorted_player[0].team.name, sorted_player[5].team.name]
        column_colors = [sorted_player[0].team.color, sorted_player[5].team.color]
        cell_colors = [column_colors]*5
        #球员姓名
        home_player_names = [' #'.join([self.player_ids_dict[player.id][0], self.player_ids_dict[player.id][1]])   for player in sorted_player[0:5]]
        guest_player_names = [' #'.join([self.player_ids_dict[player.id][0], self.player_ids_dict[player.id][1]]) for player in sorted_player[5:]]
        #制作表格
        table = plt.table(cellText = zip(home_player_names, guest_player_names), colLabels = column_labels, colColours = column_colors, colWidths = [Constant.COL_WIDTH,Constant.COL_WIDTH], loc = 'bottom', cellColours=cell_colors, fontsize = Constant.FONTSIZE, cellLoc = 'center')

        #table继承于artist，继承其方法
        table.scale(1, Constant.SCALE)
        table_cells = table.properties()['child_artists']
        for cell in table_cells:
            cell._text.set_color('white')

        #这里注意ax.plot()返回的是一个列表，需要加[0]才是其中一个元素
        player_circles = [ax.plot([0],[0],[0],'o',c = player.color,markersize = Constant.PLAYER_CIRCLE_SIZE*10)[0] for player in start_moment.players]


        ball_circle = ax.plot([0],[0],[0],'o',c = start_moment.ball.color,markersize = Constant.PLAYER_CIRCLE_SIZE*8)[0]



        anim = animation.FuncAnimation(
            fig, self.update_radius,
            fargs=(player_circles, ball_circle, annotations, clock_info, ax),
            #fargs=(player_circles, ball_circle, clock_info),
            frames=len(self.moments), interval=Constant.INTERVAL)


        court = read_png("./data/bg.png")
        print court.shape

        stepX, stepY = 100.0/court.shape[1], 50.0/court.shape[0]

        X1 = np.arange(0,100,stepX)
        Y1 = np.arange(0,50,stepY)
        X1, Y1 = np.meshgrid(X1,Y1)

        ax.plot_surface(X1,Y1,np.atleast_2d(0.0), rstride = 1, cstride=1,  facecolors = court, shade = False)

        plt.show()

