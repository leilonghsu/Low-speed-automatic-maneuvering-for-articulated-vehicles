import random
import math
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

N_SAMPLE = 500
N_KNN = 10
MAX_EDGE_LEN = 30.0


class KDTree:
    def __init__(self, data):
        self.tree = scipy.spatial.cKDTree(data)

    def search(self, inp, k=1):
        if len(inp.shape) >= 2:
            index = []
            dist = []

            for i in inp.T:
                idist, iindex = self.tree.query(i, k=k)
                index.append(iindex)
                dist.append(idist)

            return index, dist
        else:
            dist, index = self.tree.query(inp, k=k)
            return index, dist


def is_collision(sx, sy, gx, gy, rr, obstacles_tree):
    x = sx
    y = sy
    dx = gx - sx
    dy = gy - sy
    yaw = math.atan2(gy - sy, gx - sx)
    d = math.sqrt(dx**2 + dy**2)

    if d >= MAX_EDGE_LEN:
        return True

    D = rr
    nstep = round(d / D)

    for i in range(nstep):
        idxs, dist = obstacles_tree.search(np.array([x, y]).reshape(2, 1))
        if dist[0] <= rr:
            return True
        x += D * math.cos(yaw)
        y += D * math.sin(yaw)

    idxs, dist = obstacles_tree.search(np.array([gx, gy]).reshape(2, 1))
    if dist[0] <= rr:
        return True

    return False


def generate_roadmap(sample_x, sample_y, rr, obstacles_tree):
    road_map = []
    nsample = len(sample_x)
    skdtree = KDTree(np.vstack((sample_x, sample_y)).T)

    for (i, ix, iy) in zip(range(nsample), sample_x, sample_y):

        index, dists = skdtree.search(
            np.array([ix, iy]).reshape(2, 1), k=nsample)
        inds = index[0]
        edge_id = []

        for ii in range(1, len(inds)):
            nx = sample_x[inds[ii]]
            ny = sample_y[inds[ii]]

            if not is_collision(ix, iy, nx, ny, rr, obstacles_tree):
                edge_id.append(inds[ii])

            if len(edge_id) >= N_KNN:
                break

        road_map.append(edge_id)

    return road_map


def random_points(sx, sy, gx, gy, rr, ox, oy, obstacles_tree):
    maxx = max(ox)
    maxy = max(oy)
    minx = min(ox)
    miny = min(oy)

    sample_x, sample_y = [], []

    while len(sample_x) <= N_SAMPLE:
        tx = (random.random() - minx) * (maxx - minx)
        ty = (random.random() - miny) * (maxy - miny)

        index, dist = obstacles_tree.search(np.array([tx, ty]).reshape(2, 1))

        if dist[0] >= rr:
            sample_x.append(tx)
            sample_y.append(ty)

    sample_x.append(sx)
    sample_y.append(sy)
    sample_x.append(gx)
    sample_y.append(gy)

    return sample_x, sample_y


def dijkstra_phase(sx, sy, gx, gy, ox, oy, rr, road_map, sample_x, sample_y):
    #TODO
    return True


def construction_phase(sx, sy, gx, gy, ox, oy, robot_size):
    obstacles_tree = KDTree(np.vstack((ox, oy)).T)

    sample_x, sample_y = random_points(sx, sy, gx, gy, robot_size, ox, oy, obstacles_tree)

    plt.plot(sample_x, sample_y, ".b")

    road_map = generate_roadmap(sample_x, sample_y, robot_size, obstacles_tree)

    rx, ry = dijkstra_phase(sx, sy, gx, gy, ox, oy, robot_size, road_map, sample_x, sample_y)

    return rx, ry


def main():
    sx = 1
    sy = 1
    gx = 9
    gy = 4
    robot_size = 5.0  # TODO

    ox = [1, 1, 1, 4, 4, 8, 8, 8]
    oy = [3, 4, 5, 1, 2, 4, 5, 6]

    plt.plot(ox, oy, ".k")
    plt.plot(sx, sy, "^r")
    plt.plot(gx, gy, "^c")
    plt.grid(True)
    plt.axis("equal")

    rx, ry = construction_phase(sx, sy, gx, gy, ox, oy, robot_size)

    plt.plot(rx, ry, "-r")
    plt.show()


main()
