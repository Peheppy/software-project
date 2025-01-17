from utils.Point import Point
from utils.ssl import Navigation

class FieldManeager():
    def __init__(self):
        self.blue_agents = {}
        self.yellow_agents = {}
        self.targets = {}

    def update_pos_blue(self, id:int, pos:Point):
        self.blue_agents[id] = Point(
            round(pos.x,1),
            round(pos.y,1)
        )

    def update_pos_yellow(self, id:int, pos):
        self.yellow_agents[id] = Point(
            round(pos.x,1),
            round(pos.y,1)
        )

    def update_pos_target(self, id:int, pos):
        self.targets[id] = Point(
            round(pos.x,1),
            round(pos.y,1)
        )

