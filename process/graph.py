import math


class Graph:
    def __init__(self, map_data:list):
        self.map_data:list = map_data
        self.height:int = len(map_data)
        self.width:int = len(map_data[0])


    def _is_valid_move(self, x:int, y:int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map_data[y][x] == ' ' or self.map_data[y][x] == 'S' or self.map_data[y][x] == 'G' or self.map_data[y][x] == 255

        return False


    def create_graph(self) -> list:
        graph:dict = {}
        moves:list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for y in range(self.height):
            for x in range(self.width):
                if self.map_data[y][x] == ' ' or self.map_data[y][x] == 'S' or self.map_data[y][x] == 'G' or self.map_data[y][x] == 255:
                    nb = [ (x + dx, y + dy) for dx, dy in moves if self._is_valid_move(x + dx, y + dy) ]
                    graph[(x, y)] = nb

        return graph


