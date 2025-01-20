from utils.Point import Point
from utils.FieldGrid import FieldGrid

import heapq    

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = self.g = float("inf")
        self.h = 0

class AStarSearch(FieldGrid):
    def __init__(self):
        super().__init__()
        
    def __update_cell_details(self, cell:Cell, p:list[int,int], g:int = 0, h:int = 0):
        cell.g = g
        cell.h = h
        cell.f = g + h
        cell.parent_i = p[0]
        cell.parent_j = p[1]

    def __unblock_agent(self, grid:list, pos:list[int,int]):
        if grid[pos[0]][pos[1]] == False:
            grid[pos[0]][pos[1]] = True
            for n in self.get_neighbors(pos[0],pos[1]):
                grid[n[0]][n[1]] = True

    def __expand_unblocked_region(self, grid:list, pos:list[int,int]):
        corner_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in corner_directions:
            corner_i = pos[0] + dir[0]
            corner_j = pos[1] + dir[1]
            if self.is_valid(corner_i, corner_j):
                grid[corner_i][corner_j] = True
            for n in self.get_neighbors(corner_i, corner_j):
                if self.is_valid(n[0], n[1]):
                    grid[n[0]][n[1]] = True        

    def __get_unblock_target_point(self, grid:list, pos:list[int,int]):
        # if target is whithin an obstacle 
        if grid[pos[0]][pos[1]] == False:
            for n in self.get_neighbors(pos[0],pos[1]):
                # return any point from target out of obstacle region 
                if grid[n[0]][n[1]] == True: return n
        # if all areas are whithin an object region, go for it
        grid[pos[0]][pos[1]] = True
        for n in self.get_neighbors(pos[0],pos[1]):
            # return any point from target out of obstacle region 
            grid[n[0]][n[1]] = True
        return pos
    
    # Trace the path from source to destination
    def trace_path(self, cell_details:list, dest:list):
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

    #COPIED AND MODIFICATED FROM https://www.geeksforgeeks.org/a-search-algorithm/
    def search(self, grid:list, src:list, dest:list):
        # makes sure that the start agent is not surrounded by itself
        self.__unblock_agent(grid,src)
        # makes sure that the target is reachable
        dest = self.__get_unblock_target_point(grid,dest)

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
            i, j = p[1], p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i, new_j = i + dir[0], j + dir[1]
                
                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        return self.trace_path(cell_details, dest)
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the new f value is smaller
                        if cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            self.__update_cell_details(cell_details[new_i][new_j],[i,j],g_new,h_new)  
        # if has not fount a path, means target and all points around it are within a obstacle
        self.__expand_unblocked_region(grid,dest)
        # tries to find a path again, now with more unblocked space around dest
        return self.search(grid,src,dest)