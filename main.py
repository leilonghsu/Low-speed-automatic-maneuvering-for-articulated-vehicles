import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from vehicle import Vehicle
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
            return float(input(prompt))
        except ValueError:
            print('That is not a valid number.')

while(True):
    vel = input_float(">>>")
    angle = input_float(">>>")
    av.move(vel,angle)
    plt.pause(1)


#
#car = Vehicle()
#car.show_random_route(fig,ax)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_xlim(0, 10)
#ax.set_ylim(0, 10)
#
#v = np.array([
#    [0.1, 1],
#    [2, 1],
#    [2, 2]
#])
#
#patch = patches.Polygon(v, closed=None, fill=None, edgecolor='r')
#
#def init():
#    ax.add_patch(patch)
#    return patch,
#
#
#def animate(i):
#    pc = 0.1
#    path = patch.get_xy()
#    point1 = path[0]
#    point2 = path[1]
#    point3 = path[2]
#    ar = [[point1[0] + pc, point1[1] + pc], [point2[0] + pc, point2[1] + pc], [point3[0] + pc, point3[1] + pc]]
#
#    patch.set_xy(np.array(ar))
#    return patch,
#
#anim = animation.FuncAnimation(fig, animate,
#                               init_func=init,
#                               frames=360,
#                               interval=1000,
#                               blit=False)
#plt.show()
#