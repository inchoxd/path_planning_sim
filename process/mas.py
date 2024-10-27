import random


class CustomerAgent:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y


    def move(self, obstacles:int, other_agents:list, width:int, height:int) -> None:
        prv_x:int = self.x
        prv_y:int = self.y
        new_x:int = self.x + random.choice([-0.1, 0.1])
        new_y:int = self.y + random.choice([-0.1, 0.1])

        if new_x < 0 or new_x > width:
            self.x = prv_x
            self.y = prv_y
            return
        if new_y < 0 or new_y > height:
            self.x = prv_x
            self.y = prv_y
            return

        for obs in obstacles:
            if obs[0] - 0.1 < new_x < obs[0] + 0.1 and obs[0] - 0.1 < new_y < obs[1] + 0.1:
                self.x = prv_x
                self.y = prv_y
                return
        for agent in other_agents:
            if new_x == agent.x and new_y == agent.y:
                self.x = prv_x
                self.y = prv_y
                return

        self.x, self.y = new_x, new_y
