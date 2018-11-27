from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

class Vehicle:
    def __init__(self):
        self.x = 300
        self.y = 200
        self.v = 0
        self.theta = 90
        
    def movement(self, vel, theta):
        self.v += vel
        self.theta += theta
        self.x1 = self.v * math.cos(self.theta)
        self.y1 = self.v * math.sin(self.theta)

    def show_random_route(self,fig,ax):
        self.fig = fig
        self.ax = ax
        chassi = Rectangle((self.x,self.y), 24.4, 78.2, self.theta, fill = False)
        self.ax.add_patch(chassi)
        
        for _ in range(10):
            #chassi.set_xy(tuple(1.1*i for i in chassi.xy))
            
            t = mpl.transforms.Affine2D().rotate_deg(-5) + self.ax.transData
            chassi.set_transform(t)
            self.theta += 10            

            plt.pause(0.1)
