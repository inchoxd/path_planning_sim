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
            

    def draw_map(self, ax=None, route:deque=None) -> None:
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


    def _is_valid_move(self, map_data:list, x:int, y:int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return map_data[y][x] != 'x'

        return False


    def create_graph(self, map_data:list) -> list:
        graph:dict = {}
        moves:list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for y in range(self.height):
            for x in range(self.width):
                if map_data[y][x] != 'x':
                    nb = [ ((x + dx, y + dy), math.sqrt(dx ** 2 + dy ** 2)) for dx, dy in moves if self._is_valid_move(map_data, x + dx, y + dy) ]
                    graph[(x, y)] = nb

        return graph


if __name__ == '__main__':
    """
    map_data = [
            'xxxxxxxxxx',
            'x        x',
            'x  xxxx  x',
            'x     x  x',
            'x S   x Gx',
            'x     x  x',
            'xxxxxxxxxx'
            ]
    """
    map_data = [
            'xxxxxxxxxxx',
            'x       xGx',
            'x xxxxx x x',
            'x     x   x',
            'x xxx xxxxx',
            'x x x     x',
            'x x xxxxx x',
            'x   x     x',
            'x xxx xxx x',
            'xS    x   x',
            'xxxxxxxxxxx',
            ]
    """
    map_data = [
            'xxxxxxxxxxxx',
            'xSx   x    x',
            'x    xxx x x',
            'x xx x   x x',
            'x      xxx x',
            'x  x xxx   x',
            'x xx x   xGx',
            'x      x xxx',
            'x xx x     x',
            'x x  xx xx x',
            'x     x    x',
            'xxxxxxxxxxxx'
            ]
    map_data = [
            'xxxxxxxxxxxx',
            'xSx        x',
            'x    xxxxx x',
            'x xx x   x x',
            'x      xxx x',
            'x  x xxx   x',
            'x xx x   xGx',
            'x      x xxx',
            'x xx x     x',
            'x x  xx xx x',
            'x     x    x',
            'xxxxxxxxxxxx'
            ]
    """
    sim = Sim(map_data)
    graph = sim.create_graph(map_data)
    sim.draw_map()
    [print(k, graph[k]) for k in graph]
    route = sim.a_star(graph)
    print(route)
    sim.draw_map(route=route)

    plt.show()
