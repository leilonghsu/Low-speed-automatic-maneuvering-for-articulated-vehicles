import math
import numpy as np
import matplotlib.patches as patches
from random import random



class ArticulatedVehicle:

    def __init__(self, plt):
        self.plt = plt
        self.velocity = 0
        self.vx = 0
        self.vy = 0
        self.trailerW = 65
        trailerH = 26
        self.headW = 30
        headH = 26
        self.startPointX = 155
        self.startPointY = 213
        #self.trailerW = 6
        #trailerH = 2
        #self.headW = 3
        #headH = 2
        #self.startPointX = 10
        #self.startPointY = 10
        self.headAngle = 0
        self.trailerAngle = 0
        self.max_v = 2
        self.max_th = 1
        self.save_hx = [self.startPointX]
        self.save_hy = [self.startPointY]
        self.save_tx = [self.startPointX - (self.headW / 2 * math.cos(np.radians(self.headAngle))) - (
                self.trailerW * math.cos(np.radians(self.trailerAngle)))]
        self.save_ty = [self.startPointY - (self.headW / 2 * math.sin(np.radians(self.headAngle))) - (
                self.trailerW * math.sin(np.radians(self.trailerAngle)))]

        hW = self.headW / 2
        hH = headH / 2
        tW = self.trailerW
        tH = trailerH / 2

        p0 = [self.startPointX + hW, self.startPointY - hH]
        p1 = [self.startPointX + hW, self.startPointY + hH]
        p2 = [self.startPointX - hW, self.startPointY + hH]
        p3 = [self.startPointX - hW, self.startPointY - hH]
        p4 = [self.startPointX - hW, self.startPointY - tH]
        p5 = [self.startPointX - hW - tW, self.startPointY - tH]
        p6 = [self.startPointX - hW - tW, self.startPointY + tH]
        p7 = [self.startPointX - hW, self.startPointY + tH]

        headVectors = np.array([p0, p1, p2, p3])
        trailerVectors = ([p4, p5, p6, p7])
        self.truckHead = patches.Polygon(headVectors, fill=None)
        self.truckTrailer = patches.Polygon(trailerVectors, fill=None)
        self.plt.gca().add_patch(self.truckHead)
        self.plt.gca().add_patch(self.truckTrailer)

    def move(self, vel, angle, dt):
        self.__updateHead(vel, angle, dt)


    def __updateHead(self, vel, angle, dt):
        self.velocity = vel

        angleChange = self.velocity / self.headW * math.tan(np.radians(angle))
        self.headAngle += angleChange

        theta = np.radians(angleChange)

        oldX = self.startPointX
        oldY = self.startPointY

        #####################
        #   X is the startPoint
        #     o------------o
        #     |            |
        #     |      X     |
        #     |            |
        #     o------------o
        self.startPointX += (dt * self.velocity) * math.cos(np.radians(self.headAngle))
        self.startPointY += (dt * self.velocity) * math.sin(np.radians(self.headAngle))

        self.save_hx.append(self.startPointX)
        self.save_hy.append(self.startPointY)

        points = self.truckHead.get_xy()
        [x, y] = points[0]

        _x = self.startPointX + (math.cos(theta) * (x - oldX)) - (math.sin(theta) * (y - oldY))
        _y = self.startPointY + (math.sin(theta) * (x - oldX)) + (math.cos(theta) * (y - oldY))

        t = np.array([_x, _y])
        newPoints = np.array([t])

        for i in range(1, len(points)):
            [x, y] = points[i]
            _x = self.startPointX + (math.cos(theta) * (x - oldX)) - (math.sin(theta) * (y - oldY))
            _y = self.startPointY + (math.sin(theta) * (x - oldX)) + (math.cos(theta) * (y - oldY))
            t = np.array([_x, _y])
            newPoints = np.append(newPoints, [t], axis=0)

        self.truckHead.set_xy(newPoints)
        self.__updateTrailer(angleChange, oldX, oldY, dt)
        print(self.headAngle)

    def __updateTrailer(self, th, oldX, oldY, dt):
        v = self.truckTrailer.get_xy()
        gamma = np.radians(self.headAngle - self.trailerAngle)

        angleChange = -th * ((1 / self.trailerW) * math.cos(gamma) + 1) - (
                (self.velocity / self.trailerW) * math.sin(gamma))

        self.trailerAngle += angleChange
        theta = -np.radians(angleChange)

        hTheta = np.radians(self.headAngle)
        tTheta = -np.radians(self.trailerAngle)
        self.save_tx.append(self.startPointX - (self.headW / 2 * math.cos(hTheta)) - (self.trailerW * math.cos(tTheta)))
        self.save_ty.append(self.startPointY - (self.headW / 2 * math.sin(hTheta)) - (self.trailerW * math.sin(tTheta)))

        [x, y] = v[0]
        _x = self.startPointX + math.cos(theta) * (x - oldX) - math.sin(theta) * (y - oldY)
        _y = self.startPointY + math.sin(theta) * (x - oldX) + math.cos(theta) * (y - oldY)

        t = np.array([_x, _y])
        newV = np.array([t])

        for i in range(1, len(v)):
            [x, y] = v[i]

            _x = self.startPointX + math.cos(theta) * (x - oldX) - math.sin(theta) * (y - oldY)
            _y = self.startPointY + math.sin(theta) * (x - oldX) + math.cos(theta) * (y - oldY)
            t = np.array([_x, _y])
            newV = np.append(newV, [t], axis=0)

        self.truckTrailer.set_xy(newV)

    def move_on_path(self, rx, ry):
        straight_movements = 0  # backward or forward
        turn_movements = 0  # right or left
        angle = 0  # TODO
        vel = 0
        for i in range((len(rx) - 1)):
            x_start = rx[i]
            y_start = ry[i]
            theta_start = 2 * np.pi * random() - np.pi #TODO
            x_goal = rx[i+1]
            y_goal = ry[i+1]
            theta_goal = 2 * np.pi * random() - np.pi #TODO
            self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal)

        return straight_movements, turn_movements

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal):
        Kp_rho = 2
        Kp_alpha = 30
        Kp_beta = -5
        dt = 0.01

        x = x_start
        y = y_start
        theta = theta_start

        x_diff = x_goal - x
        y_diff = y_goal - y

        x_traj, y_traj = [], []

        rho = np.sqrt(x_diff ** 2 + y_diff ** 2)
        while rho > 0.001:
            x_traj.append(x)
            y_traj.append(y)

            x_diff = x_goal - x
            y_diff = y_goal - y

            rho = np.sqrt(x_diff ** 2 + y_diff ** 2)
            alpha = (np.arctan2(y_diff, x_diff) -
                     theta + np.pi) % (2 * np.pi) - np.pi
            beta = (theta_goal - theta - alpha + np.pi) % (2 * np.pi) - np.pi

            v = Kp_rho * rho
            w = Kp_alpha * alpha + Kp_beta * beta

            if alpha > np.pi / 2 or alpha < -np.pi / 2:
                v = -v

            theta = theta + w * dt
            x = x + v * np.cos(theta) * dt
            y = y + v * np.sin(theta) * dt
            self.plt.pause(0.01)
            degrees = np.rad2deg(theta)
            self.move(v, degrees, dt)
        return x_traj,y_traj

    def redraw_vehicle(self, x_start, y_start):
        #av = ArticulatedVehicle(self.plt)
        self.startPointX = x_start
        self.startPointY = y_start

