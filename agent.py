from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

from field_positions import FieldManeager
from field_graph import Graph

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, fm = FieldManeager(), graph = Graph()):
        super().__init__(id, yellow)
        self.fm = fm
        self.graph = graph

    def decision(self):
        if len(self.targets) == 0:
            return
        self.fm.update_pos_blue(self.id, self.pos)

        my_pos = Point(round(self.pos.x,1),round(self.pos.y,1))

        dest_pos = Point( round(self.targets[0].x,1), round(self.targets[0].y,1))
        path = self.graph.a_star_search(self.graph.adj[my_pos],self.graph.adj[dest_pos])
        for point in path:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, point)
            self.set_vel(target_velocity)
            self.set_angle_vel(target_angle_velocity)



        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        return

    def post_decision(self):
        pass
class SecondAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, vel_mult=0.3, fm = FieldManeager()):
        super().__init__(id, yellow)
        self.vel_mult = vel_mult
        self.fm = fm

    def decision(self):
        if len(self.targets) == 0:
            return

        self.fm.update_pos_blue(self.id, self.pos)

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])

        vel_mult = self.vel_mult 
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        return

    def post_decision(self):
        pass