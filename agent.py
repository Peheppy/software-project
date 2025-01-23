from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent

from utils.FieldPositions import FieldPositions
from utils.FieldGrid import FieldGrid
from utils.PathManager import PathManager
from utils.GameManager import GameManager

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, fm = GameManager()):
        super().__init__(id, yellow)
        self.fm = fm
        self.pm = PathManager()
        self.t = FieldGrid()

    def decision(self):
        if len(self.targets) == 0:
            return
        
        self.fm.awakened_agents_ind[self.id] = True
        self.fm.update_pos_blue(self.id, self.pos)

        if self.fm.agent_has_target(self.id) and self.fm.targets[self.fm.agent_target(self.id)] in self.targets:
            target = self.fm.targets[self.fm.agent_target(self.id)]
            self.pm.go_to_target(self.pos, target, self.fm.get_other_agents(self.id), self)
        else:
            self.pm.path.clear()

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