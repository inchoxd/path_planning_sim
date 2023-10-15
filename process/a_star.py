from collections import deque
import math


class Astar:
    def __init__(self):
        self.start:tuple = (0, 0)
        self.goal:tuple = (0, 0)


    def _calc_score(self, node:tuple) -> float:
        sdx = node[0] - self.start[0] 
        sdy = node[1] - self.start[1]
        gdx = self.goal[0] - node[0] 
        gdy = self.goal[1] - node[1]
        score:float = (abs(sdx) + abs(sdy)) + math.sqrt((gdx ** 2) + (gdy ** 2))

        return score


    def a_star(self, graph:dict, start:tuple, goal:tuple) -> deque:
        self.start = start
        self.goal = goal
        node = (0, 0)
        opened:deque = deque([])
        closed:deque = deque([])
        dataset:dict = {
                'node_pos':self.start,
                'parent':self.start,
                'score':self._calc_score(self.start)
                }
        opened.append(dataset)

        i = 0
        is_goal:bool = False
        while(len(opened)):
            scores:list = [ node_data['score'] for node_data in opened ]
            nodes:list = [ opened[i] for i, v in enumerate(scores)  if v == min(scores) ]

            node:dict = {}
            for node in nodes:
                [ closed.append(node) for opn_dataset in opened if opn_dataset['node_pos'] == node['node_pos'] ]
                if node['node_pos'] == self.goal:
                    [ opened.remove(node) for cls_dataset in closed if cls_dataset['node_pos'] == node['node_pos'] ]
                    is_goal = True
                    break

                opn_poses = [ opn_dataset['node_pos'] for opn_dataset in opened ]
                cls_poses = [ cls_dataset['node_pos'] for cls_dataset in closed ]
                chld_nodes:list = graph[node['node_pos']]
                for chld_node in chld_nodes:
                    dataset = {
                            'node_pos':chld_node,
                            'parent':node['node_pos'],
                            'score':self._calc_score(chld_node)
                            }

                    if dataset['node_pos'] not in opn_poses and dataset['node_pos'] not in cls_poses:
                        opened.append(dataset)
                    else:
                        for opn_dataset, cls_dataset in zip(opened, closed):
                            if dataset['node_pos'] == opn_dataset['node_pos'] and dataset['score'] < opn_dataset['score']:
                                opened.append(dataset)
                                opened.remove(opn_dataset)
                            elif dataset['node_pos'] == cls_dataset['node_pos'] and dataset['score'] < cls_dataset['score']:
                                opened.append(dataset)
                                closed.remove(cls_dataset)
                            else:
                                pass

                [ opened.remove(node) for cls_dataset in closed if cls_dataset['node_pos'] == node['node_pos'] ]

            if is_goal:
                break

        i:int = 0
        cls_node:dict = {}
        crr_pos:tuple = (0, 0)
        next_pos:tuple = closed[-1]['node_pos']
        route:deque = deque([])

        for i in range(len(closed)):
            cls_node = closed.pop()
            crr_pos = cls_node['node_pos']
            if crr_pos == next_pos:
                next_pos = cls_node['parent']
                route.append(crr_pos)

        return route
