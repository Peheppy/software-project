from utils.Point import Point
class FieldPositions():
    def __init__(self):
        self.b_agents = [Point] * 11
        self.y_agents = [Point] * 11
        self.all_agents = [Point] * 22
        self.targets = [Point(-10,-10)] * 6
        self.v_targets = [False] * 6

    def update_pos_blue(self, id:int, pos:Point):
        self.b_agents[id] = pos
        self.all_agents[id] = pos

    def update_pos_yellow(self, id:int, pos:Point):
        self.y_agents[id] = pos
        self.all_agents[id + 11] = pos

    def update_pos_target(self, id:int, pos:Point):
        self.targets[id] = pos

    def get_other_agents(self, id:int):
        other_agents = []
        for x in range(len(self.all_agents)):
            if not x == id: other_agents.append(self.all_agents[x])
        return other_agents