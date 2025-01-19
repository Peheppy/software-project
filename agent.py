from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

from utils.FieldPositions import FieldPositions
from utils.PathManager import PathManager

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, fm = FieldPositions()):
        super().__init__(id, yellow)
        self.fm = fm
        self.pm = PathManager()
        
        self.aux_path:list[Point]
        self.aux_pos:Point

    def teste(self, start_pos:Point, dest_pos:Point):
        # verify if there not is a path already
        if not len(self.pm.path) > 0:

            self.pm.astar_search(start_pos, dest_pos, self.fm.get_other_agents(self.id), True)
            self.pm.initiate_values()

            self.aux_path = self.pm.path.copy()
            self.aux_pos = self.pos
        else:
            self.pm.astar_search(self.aux_pos, dest_pos, self.fm.get_other_agents(self.id), True)
            comparision_list = [item for item in self.pm.path if item not in self.aux_path]

            # verify if an obstacle is in the last computed path
            if len(comparision_list) > 0:
                self.pm.path.clear() # in order to go to the first verification in the method
            else:
                self.pm.follow_path(self)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        self.fm.update_pos_blue(self.id, self.pos)

        self.teste(self.pos, self.targets[0])

        return

    def post_decision(self):
        pass

class SecondAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, vel_mult=0.3, fm = FieldPositions()):
        super().__init__(id, yellow)
        self.vel_mult = vel_mult
        self.fm = fm

    def decision(self):
        if len(self.targets) == 0:
            return

        self.fm.update_pos_blue(self.id, self.pos)

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])

        vel_mult = self.vel_mult 
        #self.set_vel(target_velocity)
        #self.set_angle_vel(target_angle_velocity)
        return

    def post_decision(self):
        pass