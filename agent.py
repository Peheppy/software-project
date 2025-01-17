from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

from field_positions import FieldManeager
from field_grid import Grid

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, fm = FieldManeager()):
        super().__init__(id, yellow)
        self.fm = fm
        self.grid = Grid(self.fm)

        self.path_index = 0
        self.max_path_index = 0
        self.path = []
        self.following_path = False

    def a_star_path(self, dest_pos:Point):
        self.path = self.grid.search(self.pos,dest_pos).copy()
        self.path_index = 0
        self.max_path_index = len(self.path)
        self.following_path = True

    def follow_path(self):
        # verify if has come to the end of the path
        if self.max_path_index == self.path_index:
            self.following_path = False
        # still has points in path to go
        else:
            # verify if has reached the current objective point
            if self.pos.dist_to(self.path[self.path_index]) < 0.1:
                self.path_index += 1
            # has not reached, so it continues to go to current objective point
            else:
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.path[self.path_index]) 
                self.set_vel(target_velocity)
                self.set_angle_vel(target_angle_velocity)


    def decision(self):
        if len(self.targets) == 0:
            return
        
        self.fm.update_pos_blue(self.id, self.pos)

        if self.following_path:
            self.follow_path()
        else:
            self.a_star_path(self.targets[self.id])

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
        #self.set_vel(target_velocity)
        #self.set_angle_vel(target_angle_velocity)
        return

    def post_decision(self):
        pass