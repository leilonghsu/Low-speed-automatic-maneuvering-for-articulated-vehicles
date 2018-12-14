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
dt = now - previous_t 
previous_t = now
av.move(20,1,dt)
#526
i = 0
while(i < 400):
    i+=1
    if i < 60:
        vel = 0#input_float(">>>")
        angle = -i#input_float(">>>")
    elif i >= 60 and i < 120:
        vel = 0
        angle = i-60
    else:
        vel = 0
        angle = 60
    now = time.time()
    dt = now - previous_t 
    previous_t = now
    av.move(vel,angle,0.1)
    plt.pause(.0001)
plt.plot(av.save_hx, av.save_hy, "-r")
plt.plot(av.save_tx, av.save_ty, "-b")
plt.show()