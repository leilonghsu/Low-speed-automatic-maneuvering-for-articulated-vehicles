from random import randint
import yaml


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, x, y):
        return self.x == x and self.y == y


def random_node(plot_config: dict):
    return Node(randint(plot_config['x_axis_start'], plot_config['x_axis_end']),
                randint(plot_config['y_axis_start'], plot_config['y_axis_end']))


def is_collision_free(node1: Node, node2: Node):  #TODO
    return True


def start():
    plot_config = '../config/plot_config.yaml'
    with open(plot_config) as f:
        plot_config = yaml.load(f)

    start_node = Node(1, 1)
    goal_node = Node(9, 4)
    obstacles_x = [1, 1, 1, 4, 4, 8, 8, 8]
    obstacles_y = [3, 4, 5, 1, 2, 4, 5, 6]

    path = []

    while True:
        c = random_node(plot_config)
        c_temp = random_node(plot_config)
        if is_collision_free(c, c_temp):
            path.append()
            if c.equals(c_temp.x, c_temp.y):
                return path


start()
