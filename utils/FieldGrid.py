from utils.Point import Point
from utils.ssl.small_field import SSLHRenderField
import copy

class FieldGrid(SSLHRenderField):
    def __init__(self):
        self.row = (self.width * 10) + 1
        self.col = (self.length * 10) + 1
        self.grid = [[True for _ in range(self.col)] for _ in range(self.row)]

    def is_valid(self, row, col):
        return (row >= 0) and (row < self.row) and (col >= 0) and (col < self.col)
    def is_unblocked(self, grid, row, col):
        return grid[row][col] == True
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]
    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    def point_to_index(self, point:Point):
        # in index x and y are swapped
        return int((point.y + 2) * 10) ,int((point.x + 3) * 10) 
    
    def index_to_point(self, i:int,j:int):
        return Point(round(-3 + (0.1 * j),1), round(-2 + (0.1 * i),1))
    
    def get_neighbors(self,i, j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return [
            [i + dir[0], j + dir[1]] 
            for dir in directions 
            if self.is_valid(i + dir[0], j + dir[1])
        ]
    
    def update_blocked_cells_grid(self, obstacles_pos = []):
        # a grid is created in order to maintain the original grid "clean"
        grid = copy.deepcopy(self.grid)

        # Directions to check corners around the central position
        corner_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Process each obstacle position
        for pos in obstacles_pos:
            i, j = self.point_to_index(pos)

            # Mark the obstacle's center as blocked if valid
            if self.is_valid(i, j):
                grid[i][j] = False

            # Mark corners and their neighbors as blocked
            for dir in corner_directions:
                corner_i = i + dir[0]
                corner_j = j + dir[1]
                if self.is_valid(corner_i, corner_j):
                    grid[corner_i][corner_j] = False
                for n in self.get_neighbors(corner_i, corner_j):
                    if self.is_valid(n[0], n[1]):
                        grid[n[0]][n[1]] = False

        return grid
    