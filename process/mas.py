import random


class CustomerAgent:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y


    def move(self, obstacles:int, other_agents:list, width:int, height:int) -> None:
        width:float = round(width - 1.5, 3)
        height:float = round(height - 1.5, 3)
        new_x:float = self.x + random.choice([-0.1, 0.1])
        new_y:float = self.y + random.choice([-0.1, 0.1])

        if new_x < 0.5 or new_x > width:
            return
        if new_y < 0.5 or new_y > height:
            return

        for obs in obstacles:
            if (obs[0] - 0.5 < new_x < obs[0] + 0.5) and (obs[1] - 0.5 < new_y < obs[1] + 0.5):
                return
        for agent in other_agents:
            if new_x == agent.x and new_y == agent.y:
                return

        self.x, self.y = round(new_x, 3), round(new_y, 3)
