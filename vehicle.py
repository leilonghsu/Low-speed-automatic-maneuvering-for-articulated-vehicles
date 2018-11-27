from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib as mpl

class Vehicle:
    def __init__(self,fig,ax):
        self.fig = fig
        self.ax = ax
        chassi = Rectangle((100,100), 24.4, 78.2, fill = False)
        self.ax.add_patch(chassi)
        
        t = mpl.transforms.Affine2D().rotate_deg(-25) + self.ax.transData
        for _ in range(10):
            chassi.set_xy(tuple(1.1*i for i in chassi.xy))
            
            

            chassi.set_transform(t)

            plt.pause(0.1)
        print(chassi.xy)
