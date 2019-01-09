import matplotlib.pyplot as plt
from articulatedVehicle import ArticulatedVehicle
from probabilistic_roadmap import PRM


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
    av.move(1, 0, 0.1)

    av.move_on_path(reversed_rx, reversed_ry)
    #av.move_to_pose(10, 10, 0, 50, 50, 270)

    #print(av.truckHead.get_xy())

    plt.show()


start_prm()
