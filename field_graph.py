from utils.Point import Point
from field_positions import FieldManeager
import heapq    

class Node:
    def __init__(self, pos:Point):
        # graph variables
        self.pos = pos
        self.neighbors = []

        # a* variables
        self.g = self.f = float('inf')
        self.h = 0
        self.next_node = None
        self.unblocked = True

class Graph:
    def __init__(self, fm = FieldManeager(), collums=31, rows=21):
        self.fm = fm
        self.adj = {}
        #self.vert_dist = round(6 / collums, 1)
        self.vert_dist = 0.2

        # Create nodes and edges for each point in the grid
        for x in range(0,collums):
            for y in range(0,rows):
                pos = Point(
                    round(3 - round(x * self.vert_dist,1),1), 
                    round(2 - round(y * self.vert_dist,1),1) )
                self.adj[pos] = Node(pos)
                # Connect neighboring nodes
                self.add_neighbors(self.adj[pos])

    def add_Point(self, condition:bool, x_increment:float, y_increment:float, pos_ref:Point, node:Node):
        if(condition):
            new_pos = Point(
                round(pos_ref.x + x_increment,1), 
                round(pos_ref.y + y_increment, 1))
            #self.adj[pos_ref].neighbors.append(new_pos)
            node.neighbors.append(new_pos)

    def add_neighbors(self, node:Node):
        pos = node.pos

        self.add_Point(pos.x < 3, self.vert_dist, 0.0, pos, node)# Right neighbor
        self.add_Point(pos.x < -3, -self.vert_dist, 0.0, pos, node)# Left neighbor
        self.add_Point(pos.y > -2, 0.0, -self.vert_dist, pos, node)# Upper neighbor
        self.add_Point(pos.y < 2, 0.0, self.vert_dist, pos, node)# Lower neighbor
        
        self.add_Point((pos.x < 3 and pos.y > -2), self.vert_dist, -self.vert_dist, pos, node) # Right and Upper
        self.add_Point((pos.x < 3 and pos.y < 2), self.vert_dist, self.vert_dist, pos, node) # Right and Lower
        self.add_Point((pos.x > -3 and pos.y > -2), -self.vert_dist, -self.vert_dist, pos, node) # Left and Upper
        self.add_Point((pos.x > -3 and pos.y < 2), -self.vert_dist, self.vert_dist, pos, node) # Left and Lower
    
    def add_node(self, node_pos:Point):
        #add node and its neighbors in adj set
        if node_pos not in self.adj:
            self.adj[node_pos] = Node(node_pos)
            self.add_neighbors(self.adj[node_pos])

        #add node in neighbors lists
        for neighbor in self.adj[node_pos].neighbors:
            if node_pos not in self.adj[neighbor].neighbors:
                self.adj[neighbor].neighbors.append(node_pos)
    
    def sub_node(self, node:Node):
        if node.pos in self.adj:
            #subtract node from its neighbors
            for neighbor in self.adj[node.pos].neighbors:
                self.adj[neighbor].neighbors.remove(node.pos)

            #subtract node from adj set
            del self.adj[node.pos]

    def closest_node(self, pos:Point):
        node:Node
        if pos in self.adj:
            node = self.adj[pos]
        else:
            for positive in range(0,2):
                if Point(round(pos.x + 0.1,1) * -1**positive, pos.y * -1**positive) in self.adj:
                    node = self.adj[Point(round(pos.x + 0.1,1) * -1**positive, pos.y * -1**positive)]
                    continue
                elif Point(pos.x * -1**positive, round(pos.y + 0.1,1) * -1**positive) in self.adj:
                    node = self.adj[Point(pos.x * -1**positive, round(pos.y + 0.1,1) * -1**positive)]
                    continue
                elif Point(round(pos.x + 0.1,1) * -1**positive, round(pos.y + 0.1,1) * -1**positive) in self.adj:
                    node = self.adj[Point(round(pos.x + 0.1,1), round(pos.y + 0.1,1))]
                    continue
        return node

    def trace_path(self, node:Node, start_pos:Point, dest_pos:Point):
        path = []
        current = node

        path.append(dest_pos)

        while not current.pos == start_pos:
            path.append(current.pos)
            current = current.next_node
            
        # the origin pos is not needed
        # path.append(current.pos)

        path.reverse()

        return path

    def a_star_search(self, start_node_pos:Point, dest_node_pos:Point, blocked_positions = []):

        my_blocked_pos = []
        for pos in blocked_positions:
            my_blocked_pos.append(self.closest_node(pos).pos)

        start_node = self.closest_node(start_node_pos)
        dest_node = self.closest_node(dest_node_pos)

        # for cleaning later
        nodes_visited = []

        # define which positions are blocked
        yellow_pos = []
        for yellow in self.fm.yellow_agents:
            yellow_pos.append(self.fm.yellow_agents[yellow])
            self.adj[self.closest_node(self.fm.yellow_agents[yellow]).pos].unblocked = False


        path = []

        found = False

        if start_node.pos == dest_node.pos:
            found = True
            path = [start_node.pos]

        # assign start_node with g = 0 (dist from itself) and h = dist to target
        start_node.g = 0
        start_node.h = start_node.pos.dist_to(dest_node.pos)
        start_node.f = start_node.g + start_node.h

        random_id = 0 # used for heappop/push comparision, for when node.f is equal
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, ((start_node.f, random_id), start_node))

        while len(open_list) > 0 and not found:
            #  _, ?
            _, current_node = heapq.heappop(open_list)

            nodes_visited.append(current_node)

            closed_list.add(current_node.pos)

            if current_node.pos == dest_node.pos:
                path = self.trace_path(current_node,start_node.pos, dest_node_pos)
                found = True
                continue

            for neighbor_pos in current_node.neighbors:
                random_id += 1 # for comparing in heappop/push

                neighbor_node = self.adj[neighbor_pos]

                nodes_visited.append(neighbor_node)

                #if neighbor_pos in closed_list or not neighbor_node.unblocked:
                #    continue
                if neighbor_pos in closed_list or neighbor_pos in blocked_positions:
                    continue

                g_new = current_node.g + 1.0
                h_new = neighbor_pos.dist_to(dest_node.pos)
                f_new = g_new + h_new

                if neighbor_node.f > f_new:
                    # assign neighbors dist to origin and dist
                    neighbor_node.f = f_new
                    neighbor_node.g = g_new
                    neighbor_node.h = h_new
                    neighbor_node.next_node = current_node

                    heapq.heappush(open_list, ((neighbor_node.f, random_id), neighbor_node))
        # after search, reset blocked nodes
        for x in yellow_pos:
            self.adj[self.closest_node(x).pos].unblocked = True

        # clean grid after a* search
        for x in nodes_visited:
            self.adj[x.pos].f = self.adj[x.pos].g = float("inf")
            self.adj[x.pos].h = 0
            self.adj[x.pos].next_node = None
        
        return path