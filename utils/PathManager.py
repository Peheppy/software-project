from utils.Point import Point
from utils.FieldGrid import FieldGrid
import heapq    

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = self.g = float("inf")
        self.h = 0

class PathManager(FieldGrid):
    def __init__(self):
        super().__init__()
    
    def __update_cell_details(self, cell, p, g = 0, h = 0):
        cell.g = g
        cell.h = h
        cell.f = g + h
        cell.parent_i = p[0]
        cell.parent_j = p[1]

    def __is_next_point_continuous(self, point_i:Point, point_f:Point):
        i_i, j_i = self.point_to_index(point_i)
        i_f, j_f = self.point_to_index(point_f)

        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dir in directions:
            if i_f == i_i + dir[0] and j_f == j_i + dir[1]: 
                return True
        return False
    
    # Trace the path from source to destination
    def trace_path(self,cell_details, dest):
        path = []
        row = dest[0]
        col = dest[1]
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):  # Continue until the source cell
            path.append([row, col])
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col
        #path.append([row, col])  # Add the source cell
        path.reverse()  # Reverse the path to get it from source to destination

        return path
    
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

    #COPIED AND MODIFICATED FROM https://www.geeksforgeeks.org/a-search-algorithm/
    def __astar_search_aux(self, grid:list, src:list, dest:list):

        corner_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # makes sure that the start agent is not surrounded by itself
        # makes sure that the target is reachable
        for pos in [src, dest]:
            for dir in corner_directions:
                corner_i = pos[0] + dir[0]
                corner_j = pos[1] + dir[1]
                if self.is_valid(corner_i, corner_j):
                    grid[corner_i][corner_j] = True
                for n in self.get_neighbors(corner_i, corner_j):
                    if self.is_valid(n[0], n[1]):
                        grid[n[0]][n[1]] = True

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.col)] for _ in range(self.row)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.col)] for _ in range(self.row)]

        # Initialize the start cell details
        i = src[0]
        j = src[1]
        self.__update_cell_details(cell_details[i][j], src)

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Main loop of A* search algorithm
        while open_list:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]
                
                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        # Trace and print the path from source to destination
                        return self.trace_path(cell_details, dest)
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            self.__update_cell_details(cell_details[new_i][new_j],[i,j],g_new,h_new)   

    def astar_search(self, src_pos:Point, dest_pos:Point, obstacles_pos = []):
        #obstacles_pos does NOT have agent
        src = self.point_to_index(src_pos)
        dest = self.point_to_index(dest_pos)

        updated_grid = self.update_blocked_cells_grid(obstacles_pos)
        
        index_path = self.__astar_search_aux(updated_grid,src,dest)
        point_path = [self.index_to_point(cell[0],cell[1]) for cell in index_path]
        
        # this makes sure that the target will be touched
        point_path.append(dest_pos)

        del updated_grid
        return point_path
