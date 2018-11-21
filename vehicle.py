from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
class Vehicle:
    fig,ax = plt.subplots(1)
    chassi = Rectangle((0.1,0.1), 0.0244, 0.0782, fill = False)
    ax.add_patch(chassi)
    plt.draw()
    k = True
    for n in range(10):
        chassi.set_xy(tuple(1.1*i for i in chassi.xy))
        plt.pause(0.1)
    #fig.canvas.draw_idle()
    print(chassi.xy)
    plt.show()
