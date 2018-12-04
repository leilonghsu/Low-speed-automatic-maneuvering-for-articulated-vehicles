import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np
import matplotlib.patches as patches

class ArticulatedVehicle:

    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.velocity = 0
        self.trailerW = 65
        trailerH = 26
        self.headW = 30
        headH = 26
        self.startPointX = 155
        self.startPointY = 113
        self.lineW = 10
        self.headAngle = 0
        self.trailerAngle = 0



        hW = self.headW / 2
        hH = headH / 2
        tW = self.trailerW
        tH = trailerH / 2

        p0 = [self.startPointX + hW, self.startPointY - hH]
        p1 = [self.startPointX + hW, self.startPointY + hH]
        p2 = [self.startPointX - hW, self.startPointY + hH]
        p3 = [self.startPointX - hW, self.startPointY - hH]
        p4 = [self.startPointX - hW, self.startPointY]
        p5 = [self.startPointX - hW - self.lineW, self.startPointY]
        p6 = [self.startPointX - hW - self.lineW, self.startPointY - tH]
        p7 = [self.startPointX - hW - self.lineW - tW, self.startPointY - tH]
        p8 = [self.startPointX - hW - self.lineW - tW, self.startPointY + tH]
        p9 = [self.startPointX  - hW - self.lineW, self.startPointY + tH] 

        vectors = np.array([p0,p1,p2,p3,p0,p3,p4,p5,p6,p7,p8,p9,p5])
        self.truck = patches.Polygon(vectors, fill=None, closed=None)
        ax.add_patch(self.truck)

    
    def move(self, vel, angle, delta_t):
        self.__updateHead(vel,angle, delta_t)


    def __updateHead(self,vel,angle, delta_t):
        #self.velocity += vel
        #self.headAngle += angle
        #radians = np.deg2rad(self.headAngle)

        gamma = np.deg2rad(self.headAngle - self.trailerAngle)
        angleChange = (self.velocity * delta_t * math.sin(gamma) + self.trailerW * angle)/(self.headW * math.cos(gamma) + self.trailerW)
        self.headAngle += angleChange
        radians = np.deg2rad(self.headAngle)
        
        x1 = self.velocity * math.cos(radians) * delta_t
        y1 = self.velocity * math.sin(radians) * delta_t
        self.startPointX += x1
        self.startPointY += y1
        v = self.truck.get_xy()
        [x,y] = v[0]
        _x = self.startPointX + math.cos(radians) * (x - self.startPointX) - math.sin(radians) * (y - self.startPointY)
        _y = self.startPointY + math.sin(radians) * (x - self.startPointX) + math.cos(radians) * (y - self.startPointY)
        t = np.array([_x,_y])
        newV = np.array([t])
        for i in range(1,6):
            [x,y] = v[i]
            _x = self.startPointX + math.cos(radians) * (x - self.startPointX) - math.sin(radians) * (y - self.startPointY)
            _y = self.startPointY + math.sin(radians) * (x - self.startPointX) + math.cos(radians) * (y - self.startPointY)
            t = np.array([_x,_y])
            print(t,v[i])
            newV = np.append(newV, [t], axis=0)
        self.truck.set_xy(newV)
        #self.__updateTrailer(angle, delta_t)

    #def __updateTrailer(self,g, delta_t):
    #    (x1,y1) = self.head.xy
#
    #    radians1 = np.deg2rad(self.headAngle)
    #    gamma = np.deg2rad(self.headAngle - self.trailerAngle)#180 - abs(abs(self.headAngle - self.trailerAngle) - 180)
    #    angleChange = (self.velocity * delta_t * math.sin(gamma) - self.headW * g * math.cos(gamma))/(self.headW * math.cos(gamma) + self.trailerW)
#
    #    print("Angle change of trailer: ",angleChange)
    #    print("Trailer angle: ", self.trailerAngle)
    #    print("Head angle: ", self.headAngle)
#
    #    self.trailerAngle += angleChange
    #    radians2 = np.deg2rad(self.trailerAngle)
    #    x2 = x1 - self.lineW * math.cos(radians1) - self.trailerW * math.cos(radians2)
    #    y2 = y1 - self.lineW * math.sin(radians1) - self.trailerW * math.sin(radians2)
    #    
    #    _x = x2 + (self.trailerH * 0.5)
    #    _y = y2
#
    #    self.trailer.set_xy((x2,y2))
    #    t = mpl.transforms.Affine2D().rotate_around(_x,_y,radians2) + plt.gca().transData
    #    self.trailer.set_transform(t)
#