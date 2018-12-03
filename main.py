import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from articulatedVehicle import ArticulatedVehicle
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as patches

img=mpimg.imread('firstedit.png')

fig,ax = plt.subplots(1)
imgplot = ax.imshow(img)
av = ArticulatedVehicle(fig,ax)


def input_float(prompt):
    while True:
        try:
            x = input(prompt)
            if x == "": 
                return 0
            return float(x)
        except ValueError:
            print('That is not a valid number.')

while(True):
    vel = input_float(">>>")
    angle = input_float(">>>")
    av.move(vel,angle)
    plt.pause(1)