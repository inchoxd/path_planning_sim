import random


class CustomerAgent:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y


    def move(self, obstacles:int, other_agents:process.mas.CustomerAgent, width:int, height:int) -> None:
        new_x:int = self.x + random.choice([0, 0.5])
        new_y:int = self.y + random.choice([0, 0.5])

        if new_x < 0 or new_x >= width:
            return
        if new_y < 0 or new_y >= height:
            return

        for obs in obstacles:
            if new_x == obs[0] and new_y == obs[1]:
                return
        for agent in other_agents:
            if new_x == agent.x and new_y == agent.y:
                return

        self.x, self.y = new_x, new_y
