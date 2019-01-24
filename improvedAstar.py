import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from operator import attrgetter
from articulatedVehicle import ArticulatedVehicle
import time

class Node:
    def __init__(self, x, y,gscore, fscore):
        self.x = x
        self.y = y
        self.gscore = gscore
        self.fscore = fscore



def reconstructPath(cameFrom, current):
    #print("reconstructing from ", current.x,current.y)
    totalPath = []
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.append(current)
    return list(reversed(totalPath))

def a_star(start,goal,graph):
    closedNodes, openNodes = dict(), dict()
    openNodes[calc_index(start)] = start
    cameFrom = {}
    motion = get_motion_model()
    while openNodes:
        id = min(openNodes, key=lambda o: openNodes[o].fscore)
        current = openNodes[id]

        if current.x == goal.x and current.y == goal.y:
            return reconstructPath(cameFrom, current)

        del openNodes[id]
        closedNodes[id] = current

        for i in range(len(motion)):
            node = Node(current.x + motion[i][0],
                        current.y + motion[i][1],
                        current.gscore + motion[i][2],
                        0)
            
            n_id = calc_index(node)
            if n_id in closedNodes:
                continue

            if not verify_node(node,graph):
                continue
            
            node.fscore = node.gscore + calcHeuristic(goal, node)

            if n_id not in openNodes:
                openNodes[n_id] = node
            else:
                if openNodes[n_id].gscore >= node.gscore:
                    openNodes[n_id] = node

            cameFrom[node] = current
            #plt.plot(node.x,node.y,"xc")
            #plt.pause(0.0001)

def calc_index(node):
    return node.y * 1152 + node.x

def calcHeuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def verify_node(node,graph):
    #check that the vehicle can squeeze through
    for i in range(16):
        pos1 = graph[node.y+i][node.x+i]
        pos2 = graph[node.y-i][node.x-i]
        pos3 = graph[node.y][node.x-i]
        pos4 = graph[node.y][node.x+i]
        pos5 = graph[node.y-i][node.x]
        pos6 = graph[node.y+i][node.x]
        if pos1[0] == 0 or pos2[0] == 0 or pos3[0] == 0 or pos4[0] == 0 or pos5[0] == 0 or pos6[0] == 0:
            return False
    return True


def get_motion_model():
    # dx, dy, cost
    motion = [[1, 0, 1],
              [0, 1, 1],
              [-1, 0, 1],
              [0, -1, 1],
              [-1, -1, math.sqrt(2)],
              [-1, 1, math.sqrt(2)],
              [1, -1, math.sqrt(2)],
              [1, 1, math.sqrt(2)]]

    return motion

def paint(nodeList, c):
    xs = []
    ys = []
    for n in nodeList:
        xs.append(n.x)
        ys.append(n.y)
    plt.plot(xs,ys,c)
        
def improved_astar(start,goal,graph):
    p = a_star(start,goal,graph)
    paint(p,"-r")
    if len(p) > 2:
        for index, node in enumerate(p):
            if index <= len(p)-2:
                i = 2
                len(p)
                while True:
                    if (index+i < len(p)-2):
                        dtwo = p[index+i]
                        if verify_line(node,dtwo,graph):
                            del p[index+i-1]
                        else:
                            break
                        i += 1
                    else:
                        break

    return p

def verify_line(startn,endn,graph):
    if startn.x == endn.x or startn.y == endn.y:
        return True
    M = (startn.y-endn.y)/(startn.x-endn.x)
    B = (startn.x*startn.y - endn.x*startn.y)/(startn.x-endn.x)
    x = startn.x
    if x < endn.x:
        while x < endn.x:
            y = M*x + B
            if y < 0:
                return True
            for i in range(16):
                pos1 = graph[int(y)+i][x+i]
                pos2 = graph[int(y)-i][x-i]
                pos3 = graph[int(y)][x-i]
                pos4 = graph[int(y)][x+i]
                pos5 = graph[int(y)-i][x]
                pos6 = graph[int(y)+i][x]
                if pos1[0] == 0 or pos2[0] == 0 or pos3[0] == 0 or pos4[0] == 0 or pos5[0] == 0 or pos6[0] == 0:
                    return False  
            x += 1
    else:
        while x > endn.x:
            y = M*x + B
            for i in range(16):
                pos1 = graph[int(y)+i][x+i]
                pos2 = graph[int(y)-i][x-i]
                pos3 = graph[int(y)][x-i]
                pos4 = graph[int(y)][x+i]
                pos5 = graph[int(y)-i][x]
                pos6 = graph[int(y)+i][x]
                if pos1[0] == 0 or pos2[0] == 0 or pos3[0] == 0 or pos4[0] == 0 or pos5[0] == 0 or pos6[0] == 0:
                    return False
            x -= 1

    return True

def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('That is not a valid number.')

def main():
    graph=mpimg.imread('firstedit.png')
    fig,ax = plt.subplots(1)
    imgplot = ax.imshow(graph)
    av = ArticulatedVehicle(plt)
    goal = Node(1046,30,0,0)
    start = Node(200,480,0,0)
    nodelist = improved_astar(start,goal,graph)
    paint(nodelist, "-b")
    #paint(nodelist,"xc")
    i = 0
    while(i < 400):
        i+=1
        if i < 60:
            vel = 20
            angle = -i
        elif i >= 60 and i < 120:
            vel = 20
            angle = i-60
        else:
            vel = 20
            angle = 60
        av.move(vel,angle,0.1)
        plt.pause(.0001)
    #while(i < 400):
    #    vel = 20
    #    angle = input_float(">>>")
    #    av.move(vel,angle,0.1)
    #    plt.pause(.0001)
    plt.show()

main()