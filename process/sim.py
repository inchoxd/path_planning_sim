import math
import numpy as np
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fanim

from .graph import Graph
from .mas import CustomerAgent


class Sim:
    def __init__(self, map_data:list, start:tuple, goal:tuple, num_steps:int=0, mas_customers:int=0) -> None:
        self.height:int = len(map_data)
        self.width:int = len(map_data[0])
        self.data:list = [ [ [ 255, 255, 255 ] for j in range(self.width) ] for i in range(self.height) ]
        self.wall:int = [0, 0, 0]
        self.keep_out = [51, 51, 51]
        self.speed_constrains = [204, 204, 204]
        self.pause = [204, 204, 200]

        x:int = 0
        y:int = 0
        horizontal:str = ''
        block:str = ''
        self.start:tuple = start
        #self.start:tuple = (13, 1)
        #self.start:tuple = (14, 19)
        self.goal:tuple = goal
        #self.goal:tuple = (5, 10)
        #self.goal:tuple = (3, 9)
        self.update_times:int = 0

        self.mas_customers:int = mas_customers
        self.num_steps:int = num_steps

        if mas_customers > 0:
            self.mas_customers = mas_customers
            self.graph:process.graph.Graph = Graph(map_data)
            self.obstacles:list = self.graph.get_obstacles()
            self.num_steps:int = num_steps
            self.agents:list = [ CustomerAgent(1, 1) for _ in range(mas_customers) ] 
            self.position_over_time:list = []

        for y, horizontal in enumerate(map_data):
            for x, block in enumerate(horizontal):
                if block == 'x':
                    self.data[y][x] = self.wall
                elif block == 'S':
                    self.start:tuple = (x, y)
                elif block == 'G':
                    self.goal:tuple = (x, y)
                elif block == 0:
                    self.data[y][x] = self.wall
                elif block == 204:
                    self.data[y][x] = self.speed_constrains
                elif block == 51:
                    self.data[y][x] = self.keep_out


    def _update_positions(self) -> list:
        for agent in self.agents:
            agent.move(self.obstacles, [ a for a in self.agents if a != agent ], self.width, self.height)

        return [ (agent.x, agent.y) for agent in self.agents ]


    def _update_customers(self) -> None:
        for step in range(self.num_steps):
            positions:list = self._update_positions()
            self.position_over_time.append(positions)


    def _animated_mas(self, frame:int) -> None:
        location = self.customers.pop(0)
        location.remove()
        x_values, y_values = zip(*self.position_over_time[frame])
        self.customers = self.ax.plot(x_values, y_values, 'yo', ms=8, mew=0, mfc='red')


    def _update(self, frames) -> None:
        if frames >= len(self.draw_router):
            return None
        if self.update_times > 0:
            pos = self.draw_router.popleft()
            location = self.sc_rbt.pop(0)
            location.remove()
            self.sc_rbt = self.ax.plot(pos[0], pos[1], 'yo', ms=14, mew=0, mfc='black')

        self.update_times += 1


    def _draw_map(self, route:deque, show_route:bool, animation:bool, graph:dict, mode:bool) -> fanim:
        fig, self.ax = plt.subplots(1, 1, figsize=(6, 6))
        if mode:
            window_title:str = "改良版A*アルゴリズム"
        else:
            window_title:str = "A*アルゴリズム"

        fig.canvas.manager.set_window_title(window_title)

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

        if animation or self.mas_customers > 0:
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
                    if graph[crr][1] < 1.0:
                        for digit in range(80):
                            if dx > 0:
                                x = crr[0] + (digit * -0.0125)
                            elif dx < 0:
                                x = crr[0] + (digit * 0.0125)
                            if dy > 0:
                                y = crr[1] + (digit * -0.0125)
                            elif dy < 0:
                                y = crr[1] + (digit * 0.0125)
                            self.draw_router.append((x, y))
                            if len(router) <= step + 1:
                                break
                    else:
                        for digit in range(40):
                            if dx > 0:
                                x = crr[0] + (digit * -0.025)
                            elif dx < 0:
                                x = crr[0] + (digit * 0.025)
                            if dy > 0:
                                y = crr[1] + (digit * -0.025)
                            elif dy < 0:
                                y = crr[1] + (digit * 0.025)
                            self.draw_router.append((x, y))
                            if len(router) <= step + 1:
                                break

                anim = fanim(fig, self._update, frames=1, interval=20)

                return anim

            elif self.mas_customers > 0:
                self.customers = self.ax.plot(0, 0, 'yo', ms=8, mew=0, mfc='red')
                self._update_customers()
                anim = fanim(fig, self._animated_mas, frames=self.num_steps, repeat=False)

                return anim

        return None


    def show_graph(self, ax=None, route:deque=None, show_route:bool=True, animation:bool=True, graph:dict={}, mode:bool=True) -> None:
        show = self._draw_map(route, show_route, animation, graph, mode)
        plt.show()
