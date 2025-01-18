from utils.Point import Point
from utils.ssl import Navigation

from utils.FieldGrid import FieldGrid

class FieldPositions(FieldGrid):
    def __init__(self):
        self.blue_agents = [Point] * 11
        self.yellow_agents = [Point] * 11
        self.all_agents = [Point] * 22
        self.targets = [Point] * 4

    def update_pos_blue(self, id:int, pos:Point):
        self.blue_agents[id] = pos
        self.all_agents[id] = pos

    def update_pos_yellow(self, id:int, pos:Point):
        self.yellow_agents[id] = pos
        self.all_agents[id + 11] = pos

    def update_pos_target(self, id:int, pos:Point):
        self.targets[id] = pos

    def get_other_agents(self, id:int):
        other_agents = []
        for x in range(len(self.all_agents)):
            if not x == id: other_agents.append(self.all_agents[x])
        return other_agents

