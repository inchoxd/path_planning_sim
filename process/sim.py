import math
import numpy as np
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


    def _update(self, frames) -> None:
        if frames >= len(self.draw_router):
            return None
        if self.update_times > 0:
            pos = self.draw_router.popleft()
            location = self.sc_rbt.pop(0)
            location.remove()
            self.sc_rbt = self.ax.plot(pos[0], pos[1], 'yo', ms=14, mew=0, mfc='black')

        self.update_times += 1


    def _draw_map(self, route:deque, show_route, animation:bool) -> None:
        fig, self.ax = plt.subplots(1, 1, figsize=(6, 6))

        self.sc_rbt = self.ax.plot(0, 0)
        self.ax.axis('off')

        router:deque = route.copy() if animation else deque([]) 
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
            self.draw_router:deque = deque([])
            digit:int = 0
            crr:tuple = ()
            nxt:tuple = ()

            for step in range(len(router)):
                crr = router[len(router) - step - 1]
                nxt = router[len(router) - step - 2 if len(router) > step + 1 else len(router) - step - 1]
                dx:int = crr[0] - nxt[0]
                dy:int = crr[1] - nxt[1]
                x:float = float(crr[0])
                y:float = float(crr[1])
                for digit in range(40):
                    if dx > 0:
                        x = crr[0] + (digit * -0.025)
                    elif dx < 0:
                        x = crr[0] + (digit * 0.025)
                    if dy > 0:
                        y = crr[1] + (digit * -0.025)
                    elif dy < 0:
                        y = crr[1] + (digit * 0.025)
                    self.draw_router.append((round(x, 2), round(y, 2))) 
                    if len(router) <= step + 1:
                        break

            anim = fanim(fig, self._update, frames=1, interval=20)

            return anim


    def show_graph(self, ax=None, route:deque=None, show_route:bool=True, animation:bool=True) -> None:
        show = self._draw_map(route, show_route, animation)
        plt.show()
