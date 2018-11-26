import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from vehicle import Vehicle

img=mpimg.imread('parking.png')
fig,ax = plt.subplots(1)
imgplot = ax.imshow(img)

car = Vehicle(fig,ax)

# to stop plot from closing
plt.show()