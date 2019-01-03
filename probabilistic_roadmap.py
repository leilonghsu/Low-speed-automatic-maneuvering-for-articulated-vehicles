import random
import math
import numpy as np
import scipy.spatial

N_SAMPLE = 500
N_KNN = 10
MAX_EDGE_LEN = 30.0


class Node:
    def __init__(self, x, y, cost, pind):
        self.x = x
        self.y = y
        self.cost = cost
        self.pind = pind


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


class PRM:
    def __init__(self, sx, sy, gx, gy, robot_size, ox, oy):
        self.sx = sx
        self.sy = sy
        self.gx = gx
        self.gy = gy
        self.robot_size = robot_size
        self.ox = ox
        self.oy = oy

    def find_path(self):
        rx, ry = self.construction_phase()

        return rx, ry

    def is_collision(self, sx, sy, gx, gy, rr, okdtree):
        x = sx
        y = sy
        dx = gx - sx
        dy = gy - sy
        yaw = math.atan2(gy - sy, gx - sx)
        d = math.sqrt(dx ** 2 + dy ** 2)

        if d >= MAX_EDGE_LEN:
            return True

        D = rr
        nstep = round(d / D)

        for i in range(nstep):
            idxs, dist = okdtree.search(np.array([x, y]).reshape(2, 1))
            if dist[0] <= rr:
                return True
            x += D * math.cos(yaw)
            y += D * math.sin(yaw)

        idxs, dist = okdtree.search(np.array([gx, gy]).reshape(2, 1))
        if dist[0] <= rr:
            return True

        return False

    def generate_roadmap(self, sample_x, sample_y, obstacles_tree):
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

                if not self.is_collision(ix, iy, nx, ny, self.robot_size, obstacles_tree):
                    edge_id.append(inds[ii])

                if len(edge_id) >= N_KNN:
                    break

            road_map.append(edge_id)

        return road_map

    def random_points(self, obstacles_tree):
        maxx = max(self.ox)
        maxy = max(self.oy)
        minx = min(self.ox)
        miny = min(self.oy)

        sample_x, sample_y = [], []

        while len(sample_x) <= N_SAMPLE:
            tx = (random.random() - minx) * (maxx - minx)
            ty = (random.random() - miny) * (maxy - miny)

            index, dist = obstacles_tree.search(np.array([tx, ty]).reshape(2, 1))

            if dist[0] >= self.robot_size:
                sample_x.append(tx)
                sample_y.append(ty)

        sample_x.append(self.sx)
        sample_y.append(self.sy)
        sample_x.append(self.gx)
        sample_y.append(self.gy)

        return sample_x, sample_y

    def dijkstra_phase(self, road_map, sample_x, sample_y):
        nstart = Node(self.sx, self.sy, 0.0, -1)
        ngoal = Node(self.gx, self.gy, 0.0, -1)

        openset, closedset = dict(), dict()
        openset[len(road_map) - 2] = nstart

        while True:
            if len(openset) == 0:
                print("Cannot find path")
                break

            c_id = min(openset, key=lambda o: openset[o].cost)
            current = openset[c_id]

            if c_id == (len(road_map) - 1):
                print("goal is found!")
                ngoal.pind = current.pind
                ngoal.cost = current.cost
                break

            del openset[c_id]
            closedset[c_id] = current

            for i in range(len(road_map[c_id])):
                n_id = road_map[c_id][i]
                dx = sample_x[n_id] - current.x
                dy = sample_y[n_id] - current.y
                d = math.sqrt(dx ** 2 + dy ** 2)
                node = Node(sample_x[n_id], sample_y[n_id], current.cost + d, c_id)

                if n_id in closedset:
                    continue
                if n_id in openset:
                    if openset[n_id].cost > node.cost:
                        openset[n_id].cost = node.cost
                        openset[n_id].pind = c_id
                else:
                    openset[n_id] = node

        rx, ry = [ngoal.x], [ngoal.y]
        pind = ngoal.pind
        while pind != -1:
            n = closedset[pind]
            rx.append(n.x)
            ry.append(n.y)
            pind = n.pind

        return rx, ry

    def construction_phase(self):
        obstacles_tree = KDTree(np.vstack((self.ox, self.oy)).T)

        sample_x, sample_y = self.random_points(obstacles_tree)

        road_map = self.generate_roadmap(sample_x, sample_y, obstacles_tree)

        rx, ry = self.dijkstra_phase(road_map, sample_x, sample_y)

        return rx, ry
