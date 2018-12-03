import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

class ArticulatedVehicle:

    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        #self.xAxisStart = -10
        #self.xAxisEnd = 10
        #self.yAxisStart = -10
        #self.yAxisEnd = 10
        #self.ax.set_xlim(self.xAxisStart, self.xAxisEnd)
        #self.ax.set_ylim(self.yAxisStart, self.yAxisEnd)
        self.velocity = 0
        self.trailerW = 80
        self.trailerH = 24.4
        self.headW = 35
        self.headH = 20
        self.startPointX = 15
        self.startPointY = 20
        self.lineW = 10
        self.lineH = 2
        self.lineA = 0
        self.headAngle = 0
        self.trailerAngle = 0

        #assert self.startPointX >= self.xAxisStart, "The start point is out of the x axis. Try to change the inputs"
        #assert self.startPointY >= self.yAxisStart, "The start point is out of the y axis. Try to change the inputs"

        self.totalLength = self.trailerW + self.lineW + self.headW
        #assert (self.totalLength + self.startPointX) < self.xAxisEnd, "The vehicle is out of the x axis. Try to change the inputs"

        self.totalHeight = self.trailerH
        #assert (self.totalHeight + self.startPointY) < self.yAxisEnd, "The vehicle is out of the y axis. Try to change the inputs"

        middleOfTrailer = (self.trailerH / 2) + self.startPointY

        self.trailer = plt.Rectangle((self.startPointX, self.startPointY), self.trailerW, self.trailerH, fc='r')
        plt.gca().add_patch(self.trailer)

        self.line = plt.Line2D(
            ((self.trailerW + self.startPointX),
             (self.trailerW + self.startPointX + self.lineW)),
             (middleOfTrailer, middleOfTrailer),
                        self.lineH)
        plt.gca().add_line(self.line)

        self.yPositionForHead = (self.trailerH / 2) - (self.headH / 2) + self.startPointY
        self.head = plt.Rectangle((self.trailerW + self.startPointX + self.lineW, self.yPositionForHead), self.headW, self.headH, fc='r')
        
        plt.gca().add_patch(self.head)
    
    def move(self, vel, angle):
        self.__updateHead(vel,angle)
        self.__updateTrailer(angle)

        #print(self.head)

    def __updateHead(self,vel,angle):
        self.velocity += vel
        self.headAngle += angle
        _angle = np.deg2rad(self.headAngle)
        (x,y) = self.head.xy
        x1 = vel * math.cos(_angle)
        y1 = vel * math.sin(_angle)
        #print(x1,y1)
        x += x1
        y += y1
        _x = x+(self.headH*0.5)
        _y = y+(self.headW*0.5)
        
        t = mpl.transforms.Affine2D().rotate_around(_x,_y,_angle) + plt.gca().transData
        self.head.set_transform(t)
        self.head.set_xy((x,y))

    def __updateTrailer(self,g):
        (x1,y1) = self.head.xy
        _angle = np.deg2rad(self.headAngle)
        gamma = 180 - abs(abs(self.headAngle - self.trailerAngle) - 180)
        angleChange = (self.velocity * math.sin(gamma) - self.headW * g * math.cos(gamma))/(self.headW * math.cos(gamma) + self.trailerW)
        print(angleChange)

        self.trailerAngle += angleChange
        x2 = x1 - self.headW * math.cos(_angle) - self.trailerW * math.cos(_angle)
        y2 = y1 - self.headW * math.sin(_angle) - self.trailerW * math.sin(_angle)

        _x = x2 + (self.trailerH * 0.5)
        _y = y2

        t = mpl.transforms.Affine2D().rotate_around(_x,_y,_angle) + plt.gca().transData
        self.trailer.set_transform(t)
        self.trailer.set_xy((x2,y2))
