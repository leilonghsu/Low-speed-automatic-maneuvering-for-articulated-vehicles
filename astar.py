import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from operator import attrgetter
class Node:
    def __init__(self, x, y,gscore, fscore):
        self.x = x
        self.y = y
        self.gscore = gscore
        self.fscore = fscore



def reconstructPath(cameFrom, current):
    print("reconstructing from ", current.x,current.y)
    totalPath = []
    while current in cameFrom.keys():
        current = cameFrom[current]
        print(current.x,current.y)
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
            #print(graph.shape)
            if not verify_node(node,graph):#create verify function here #
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
    pos = graph[node.y][node.x]
    if pos[0] == 1:
        return True
    else:
        return False



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

def paint(nodeList):
    xs = []
    ys = []
    for n in nodeList:
        xs.append(n.x)
        ys.append(n.y)
    plt.plot(xs,ys,"-r")
        


def main():
    graph=mpimg.imread('firstedit.png')


    fig,ax = plt.subplots(1)
    imgplot = ax.imshow(graph)
    goal = Node(1046,30,0,0)
    start = Node(200,480,0,0)
    nodelist = a_star(start,goal,graph)
    print(len(nodelist))
    paint(nodelist)
    #print(graph[200][200])
    plt.show()

main()
    