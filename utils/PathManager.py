from utils.Point import Point
from rsoccer_gym.Entities import Robot
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent

from utils.FieldGrid import FieldGrid
from utils.PathSearch import AStarSearch

class PathManager(FieldGrid):
    def __init__(self):
        super().__init__()
        self.astar = AStarSearch()

        self.path_index = 0
        self.max_path_index = 0
        self.path = []

    def initiate_values(self):
        self.path_index = 0
        self.max_path_index = len(self.path)
    
    def __is_next_point_continuous(self, point_i:Point, point_f:Point):
        i_i, j_i = self.point_to_index(point_i)
        i_f, j_f = self.point_to_index(point_f)

        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dir in directions:
            if i_f == i_i + dir[0] and j_f == j_i + dir[1]: 
                return True
        return False

    def path_trim(self, path:list):
        path_index_to_trim = []

        # iterates until has seen all points
        for index in range(len(path)):
            if (index + 2) < len(path) and self.__is_next_point_continuous(path[index], path[index + 2]):
                # saves all unnecessary points
                path_index_to_trim.append(index + 1)
        
        # Remove points in reverse order to avoid index shifting 
        for index in reversed(path_index_to_trim):
            path.pop(index)

    def follow_path(self, base_agent = BaseAgent()):
        # verify if self has come to the end of the path
        if self.max_path_index == self.path_index:
            self.path.clear()
        # still has points in path to go
        else:
            # verify if self has reached the current objective point
            if base_agent.pos.dist_to(self.path[self.path_index]) < 0.15:
                self.path_index += 1
            # self has not reached, so it continues to go to current objective point
            else:
                target_velocity, target_angle_velocity = Navigation.goToPoint(base_agent.robot, self.path[self.path_index]) 
                base_agent.set_vel(target_velocity)
                base_agent.set_angle_vel(target_angle_velocity)

    def astar_search(self, src_pos:Point, dest_pos:Point, obstacles_pos = [], update_path = False):
        #obstacles_pos does NOT have agent
        src = self.point_to_index(src_pos)
        dest = self.point_to_index(dest_pos)

        updated_grid = self.update_blocked_cells_grid(obstacles_pos)
        
        index_path = self.astar.search(updated_grid, src, dest)
        point_path = [self.index_to_point(cell[0],cell[1]) for cell in index_path]
        # this makes sure that the target will be touched
        point_path.append(dest_pos)

        self.path_trim(point_path)

        if(update_path): self.path = point_path
        del updated_grid
