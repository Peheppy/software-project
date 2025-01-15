from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

from field_positions import FieldManeager

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, f_m = FieldManeager()):
        super().__init__(id, yellow)
        self.f_m = f_m

    def decision(self):
        if len(self.targets) == 0:
            return
        
        self.f_m.update_pos_blue(self.id, self.pos)

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
class SecondAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, vel_mult=0.3, f_m = FieldManeager()):
        super().__init__(id, yellow)
        self.vel_mult = vel_mult
        self.f_m = f_m

    def decision(self):
        if len(self.targets) == 0:
            return

        self.f_m.update_pos_blue(self.id, self.pos)


        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])

        vel_mult = self.vel_mult 
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        return

    def post_decision(self):
        pass