import math


class Graph:
    def __init__(self, map_data:list):
        self.map_data:list = map_data
        self.height:int = len(map_data)
        self.width:int = len(map_data[0])


    def _is_valid_move(self, x:int, y:int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map_data[y][x] == ' ' or self.map_data[y][x] == 'S' or self.map_data[y][x] == 'G' or self.map_data[y][x] > 51

        return False


    def create_graph(self, is_pls_score:bool) -> list:
        graph:dict = {}
        moves:list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for y in range(self.height):
            for x in range(self.width):
                if self.map_data[y][x] == ' ' or self.map_data[y][x] == 'S' or self.map_data[y][x] == 'G' or self.map_data[y][x] > 51:
                    nb:list = [ (x + dx, y + dy) for dx, dy in moves if self._is_valid_move(x + dx, y + dy) ]
                    if self.map_data[y][x] == 204 and is_pls_score:
                        nb = [0.0, 0.5] + nb
                    else:
                        nb = [0.0, 1.0] + nb
                    graph[(x, y)] = nb

        return graph


    def get_obstacles(self)->list:
        x:int = 0
        y:int = 0
        obstacles:list = [ (round(x, 3), round(y, 3)) for y in range(len(self.map_data)) for x in range(len(self.map_data[y])) if self.map_data[y][x] == 0 ]

        return obstacles
