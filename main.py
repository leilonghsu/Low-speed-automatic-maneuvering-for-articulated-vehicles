import matplotlib.pyplot as plt
from articulatedVehicle import ArticulatedVehicle
from probabilistic_roadmap import PRM
from improvedAstar import improved_astar, Node
import time


def start_prm():
    # sx = 1
    # sy = 1
    # gx = 9
    # gy = 4
    # robot_size = 5
    # ox = [1, 1, 1, 4, 4, 8, 8, 8]
    # oy = [3, 4, 5, 1, 2, 4, 5, 6]

    sx = 10.0  # [m]
    sy = 10.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    robot_size = 5.0  # [m]

    ox = []
    oy = []

    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(40):
        ox.append(20.0)
        oy.append(i)
    for i in range(40):
        ox.append(40.0)
        oy.append(60.0 - i)

    plt.plot(ox, oy, ".k")
    plt.plot(sx, sy, "^r")
    plt.plot(gx, gy, "^c")

    plt.grid(True)

    prm = PRM(sx, sy, gx, gy, robot_size, ox, oy)

    rx, ry = prm.find_path()
    reversed_rx = rx[::-1]
    reversed_ry = ry[::-1]

    plt.plot(rx, ry, "-r")
    av = ArticulatedVehicle(plt)
    #av.move(10, 0, 0.1)

    av.move_on_path(reversed_rx, reversed_ry)
    #av.move_to_pose(10, 10, 0, 50, 50, 270)

    #print(av.truckHead.get_xy())

    plt.show()


#start_prm()
def inputs(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('That is not a valid number.')

def move(av):
    previous_t = time.time()
    now = time.time()
    dt = now - previous_t 
    previous_t = now
    i = 0
    while(i < 180):
        i+=1
        vel = 2
        angle = inputs(">>")
        now = time.time()
        dt = now - previous_t 
        previous_t = now
        av.move(vel,angle,0.1)
        plt.pause(.0001)

def tmp():
    sx = 10.0  # [m]
    sy = 10.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    robot_size = 5  # [m]

    obstacles = []

    for i in range(60):
        obstacles.append(Node(i,0,0,0))
    for i in range(60):
        obstacles.append(Node(60,i,0,0))
    for i in range(61):
        obstacles.append(Node(i,60,0,0))
    for i in range(61):
        obstacles.append(Node(0,i,0,0))
    for i in range(40):
        obstacles.append(Node(20,i,0,0))
    for i in range(40):
        obstacles.append(Node(40,60-i,0,0))

    ox = list(o.x for o in obstacles)
    oy = list(o.y for o in obstacles)
    
    plt.plot(ox, oy, ".k")
    plt.plot(sx, sy, "^r")
    plt.plot(gx, gy, "^c")

    plt.grid(True)
    goal = Node(gx,gy,0,0)
    start = Node(sx,sx,0,0)
    nodelist = improved_astar(start,goal, robot_size, obstacles)
    av = ArticulatedVehicle(plt)
    
    nx = list(o.x for o in nodelist)
    ny = list(o.y for o in nodelist)
    
    plt.plot(nx, ny, "-b")
    #xs,ys = av.move_to_pose(av.startPointX, av.startPointY, 0, av.startPointX+50, av.startPointY+50, 45)
    #plt.plot(xs,ys,"--b")
    move(av)
    #previous_t = time.time()
    #now = time.time()
    #dt = now - previous_t 
    #previous_t = now
    #i = 0
    #while(i < 400):
    #    i+=1
    #    if i < 60:
    #        vel = 2#input_float(">>>")
    #        angle = -i#input_float(">>>")
    #    elif i >= 60 and i < 120:
    #        vel = 2
    #        angle = i-60
    #    else:
    #        vel = 2
    #        angle = 60
    #    now = time.time()
    #    dt = now - previous_t 
    #    previous_t = now
    #    av.move(vel,angle,0.1)
    #    plt.pause(.0001)
    #
    #reversed_rx = rx[::-1]
    #reversed_ry = ry[::-1]

    #plt.plot(rx, ry, "-r")

    plt.show()

tmp()