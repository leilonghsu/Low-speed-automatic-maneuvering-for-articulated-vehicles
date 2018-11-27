import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from vehicle import Vehicle
import numpy as np

img=mpimg.imread('firstedit.png')

fig,ax = plt.subplots(1)
imgplot = ax.imshow(img)

car = Vehicle(fig,ax)

# to stop plot from closing
plt.show()