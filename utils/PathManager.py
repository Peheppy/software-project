from utils.Point import Point
from utils.FieldGrid import FieldGrid

class PathManager(FieldGrid):
    def __init__(self):
        super().__init__()

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

