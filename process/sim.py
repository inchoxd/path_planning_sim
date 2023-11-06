import math
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fanim

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
        self.start:tuple = (13, 1)
        self.goal:tuple = (5, 10)
        self.update_times:int = 0

        for y, horizontal in enumerate(map_data):
            for x, block in enumerate(horizontal):
                if block == 'x':
                    self.data[y][x] = self.wall
                elif block == 'S':
                    self.start:tuple = (x, y)
                elif block == 'G':
                    self.goal:tuple = (x, y)
                elif type(block) is int and block == 0:
                    self.data[y][x] = self.wall


    def _update(self, i) -> None:
        if i >= len(self.router):
            return None
        if self.update_times > 0:

            crr:tuple = self.router[len(self.router)-i-1]
            nxt:tuple = self.router[len(self.router)-i-2 if len(self.router)>i+1 else len(self.router)-i-1]
            sc_rbt = self.ax.scatter([crr[0]], [crr[1]], c='yellow', s=300)
        self.update_times += 1


    def _draw_map(self, route:deque, show_route, animation:bool) -> None:
        fig, self.ax = plt.subplots(1, 1, figsize=(6, 6))

        self.ax.axis('off')

        self.router:deque = route.copy() if animation else deque([]) 
        if show_route:
            i:int = 0
            for i in range(len(route)):
                node:tuple = route.popleft()
                x:int = node[0]
                y:int = node[1]
                self.data[y][x] = [0, 255, 0]

        im = self.ax.imshow(self.data, origin='upper')
        sc_st = self.ax.scatter([self.start[0]], [self.start[1]], c='b', s=300)
        tx_st = self.ax.text(self.start[0], self.start[1], 'S', ha='center', va='center', fontsize=15, c='w', weight='bold')
        sc_go = self.ax.scatter([self.goal[0]],  [self.goal[1]],  c='r', s=300)
        tx_go = self.ax.text(self.goal[0],  self.goal[1],  'G', ha='center', va='center', fontsize=15, c='w', weight='bold')

        if animation:
            anim = fanim(fig, self._update)

            return anim


    def show_graph(self, ax=None, route:deque=None, show_route:bool=True, animation:bool=True) -> None:
        show = self._draw_map(route, show_route, animation)
        plt.show()
