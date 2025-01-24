from utils.Point import Point
from utils.FieldGrid import FieldGrid

import heapq    

class Cell:
    def __init__(self):
        self.parent = [int,int]
        self.f = self.g = float("inf")
        self.h = 0

class AStarSearch(FieldGrid):
    def __init__(self):
        super().__init__()
        
    def __update_cell_details(self, cell:Cell, p:list[int,int], g:int = 0, h:int = 0):
        cell.g = g
        cell.h = h
        cell.f = g + h
        cell.parent[0], cell.parent[1] = p[0], p[1] 

    # sets a target worth of grid points and its outline points as free
    def __expand_unblocked_region(self, grid:list, pos:list[int,int]):
        if grid[pos[0]][pos[1]] == False:
            corner_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in corner_directions:
                corner_i, corner_j = pos[0] + dir[0], pos[1] + dir[1]
                if self.is_valid(corner_i, corner_j):
                    grid[corner_i][corner_j] = True
                for n in self.get_neighbors(corner_i, corner_j):
                    grid[n[0]][n[1]] = True        

    # Trace the path from source to destination
    def trace_path(self, cell_details:list, dest:list):
        path = []
        row, col = dest[0], dest[1]
        # Continue until the source cell
        while not (cell_details[row][col].parent[0] == row and cell_details[row][col].parent[1] == col):  
            path.append([row, col])
            temp_row, temp_col = cell_details[row][col].parent[0], cell_details[row][col].parent[1]
            row, col = temp_row, temp_col
        
        path.reverse()  # Reverse the path to get it from source to destination

        return path

    def search(self, grid: list, src: list, dest: list, max_attempts: int = 8):

        # this makes sure both target and agent are not inside
        # another agent blocked area
        self.__expand_unblocked_region(grid, src)
        self.__expand_unblocked_region(grid, dest)

        closed_list = [[False for _ in range(self.col)] for _ in range(self.row)]
        cell_details = [[Cell() for _ in range(self.col)] for _ in range(self.row)]

        i, j = src[0], src[1]
        self.__update_cell_details(cell_details[i][j], src)

        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        while open_list:
            _, i, j = heapq.heappop(open_list)
            closed_list[i][j] = True

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i, new_j = i + dir[0], j + dir[1]

                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    if self.is_destination(new_i, new_j, dest):
                        cell_details[new_i][new_j].parent[0] = i
                        cell_details[new_i][new_j].parent[1] = j
                        return self.trace_path(cell_details, dest)

                    g_new = cell_details[i][j].g + 1.0
                    h_new = self.calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        self.__update_cell_details(cell_details[new_i][new_j], [i, j], g_new, h_new)

        # if has not found destiny, waits in position
        return [[src[0],src[1]]]
