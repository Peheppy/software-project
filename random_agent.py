from rsoccer_gym.Entities import Robot
from utils.ssl.Navigation import Navigation
from utils.Point import Point
from utils.ssl.base_agent import BaseAgent
import random

from utils.FieldPositions import FieldPositions

class RandomAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, f_m = FieldPositions(), vel_mult=0.3):
        super().__init__(id, yellow)
        self.f_m = f_m
        self.vel_mult = vel_mult

    def decision(self):
        if len(self.targets) == 0:
            return

        self.f_m.update_pos_yellow(self.id,self.pos)

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])

        vel_mult = self.vel_mult #random.uniform(0.2, 0.6)
        target_velocity = Point(target_velocity.x * vel_mult, target_velocity.y * vel_mult)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass