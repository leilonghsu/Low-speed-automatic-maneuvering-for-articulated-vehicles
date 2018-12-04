import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from articulatedVehicle import ArticulatedVehicle
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as patches
import time

img=mpimg.imread('firstedit.png')

fig,ax = plt.subplots(1)
imgplot = ax.imshow(img)
av = ArticulatedVehicle(fig,ax)

v = np.array([[10,10],[50,10]])
b = np.rot90(v)
p = patches.Polygon(b, closed=None, fill=None)
ax.add_patch(p)


def input_float(prompt):
    while True:
        try:
            x = input(prompt)
            if x == "": 
                return 0
            return float(x)
        except ValueError:
            print('That is not a valid number.')

previous_t = time.time()
now = time.time()
delta_t = now - previous_t 
previous_t = now
av.move(2,90,delta_t)
while(True):
    vel = 0#input_float(">>>")
    angle = 0.5#input_float(">>>")
    now = time.time()
    delta_t = now - previous_t 
    previous_t = now
    #av.move(vel,angle,delta_t)
    plt.pause(.5)