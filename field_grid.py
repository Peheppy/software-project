from utils.Point import Point
from field_positions import FieldManeager
import heapq    

class Node:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = self.g = float("inf")
        self.h = 0

    # Check if a cell is valid (inside grid boundaries)

ROW = 21
COL = 31

def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
    #print("The Path is:")
    path = []
    row = dest[0]
    col = dest[1]
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):  # Continue until the source cell
        path.append([row, col])
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
    path.append([row, col])  # Add the source cell
    path.reverse()  # Reverse the path to get it from source to destination

    #print(path)
    return path

def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    #if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
    #    print("Source or destination is invalid")
    #    return []

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        #return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        #return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Node() for _ in range(COL)] for _ in range(ROW)]

    path = []

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
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
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True
                    continue
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    #if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                    if cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")
    if len(path) == 0:
        print("OPA")
    return path

class Grid:
    def __init__(self, fm = FieldManeager()):
        self.fm = fm
        self.grid = [[True for _ in range(COL)] for _ in range(ROW)]

    def point_to_index(self, point:Point):
        # in index x and y are swapped
        return int((point.y + 2) * 5) ,int((point.x + 3) * 5) 
    
    def index_to_point(self, i:int,j:int):
        return Point(round(-3 + (0.2 * j),1), round(-2 + (0.2 * i),1))
    
    def update_blocked_cells(self, static = True, yellow_pos = []):
        if static:
            yellow_agents = self.fm.yellow_agents.copy()
        else:
            yellow_agents = yellow_pos.copy()

        for pos in yellow_agents:
            i, j = self.point_to_index(yellow_agents[pos])
            self.grid[i][j] = False
    
    def search(self, src_pos:Point, dest_pos:Point, static = True, yellow_pos = []):

        src = self.point_to_index(src_pos)
        dest = self.point_to_index(dest_pos)

        self.update_blocked_cells(static,yellow_pos)
        
        path = a_star_search(self.grid,src,dest)
        new_path = [self.index_to_point(cell[0],cell[1]) for cell in path]

        return new_path



