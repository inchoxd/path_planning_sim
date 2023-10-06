import math
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Sim:
    def __init__(self, map_data:list) -> None:
        self.wall:int = [0, 0, 0]
        self.height:int = len(map_data)
        self.width:int = len(map_data[0])
        self.data:list = [ [ [ 255, 255, 255 ] for j in range(self.width) ] for i in range(self.height) ]

        x:int = 0
        y:int = 0
        horizontal:str = ''
        block:str = ''

        for y, horizontal in enumerate(map_data):
            for x, block in enumerate(horizontal):
                if block == 'x':
                    self.data[y][x] = self.wall
                elif block == 'S':
                    self.start:tuple = (x, y)
                elif block == 'G':
                    self.goal:tuple = (x, y)
            

    def _draw_map(self, ax=None, route:deque=None) -> None:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        ax.axis('off')

        if route is not None:
            """
            for i, node in enumerate(route):
                x:int = node[0]
                y:int = node[1]
                self.data[y][x] = [0, 255, 0]
            """
            for i in range(len(route)):
                node:tuple = route.popleft()
                x:int = node[0]
                y:int = node[1]
                self.data[y][x] = [0, 255, 0]

        im = ax.imshow(self.data, origin='upper')
        sc_st = ax.scatter([self.start[0]], [self.start[1]], c='b', s=300)
        tx_st = ax.text(self.start[0], self.start[1], 'S', ha='center', va='center', fontsize=15, c='w', weight='bold')
        sc_go = ax.scatter([self.goal[0]],  [self.goal[1]],  c='r', s=300)
        tx_go = ax.text(self.goal[0],  self.goal[1],  'G', ha='center', va='center', fontsize=15, c='w', weight='bold')


    def show_graph(self) -> None:
        self._draw_map()
        plt.show()
