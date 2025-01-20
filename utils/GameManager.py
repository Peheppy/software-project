from utils.FieldPositions import FieldPositions
from utils.Point import Point
import heapq    

class GameManager(FieldPositions):
    def __init__(self):
        super().__init__()
        # agent_index, target_index
        self.agents_following_targets = {}
        self.idle_positions = [Point(5,10),Point(15,10),Point(25,10),
                               Point(35,10),Point(5,30),Point(5,50),
                               Point(15,30),Point(15,50),Point(25,30),
                               Point(25,50),Point(35,30)]

    def __get_agents_dists_to_target(self, target_pos:Point):
        distances = []
        for agent_index in range(len(self.blue_agents)):
            # pushes dist and agent_index
            heapq.heappush(distances, (self.blue_agents[agent_index].dist_to(target_pos), agent_index))
        return distances

    def __find_agent_to_target(self, target_id:int):
        distances = self.__get_agents_dists_to_target(self.targets[target_id])

        while len(distances) > 0: 
            closest_agent = heapq.heappop(distances)
            agent_id = closest_agent[1]

            # verify if agent is not following any target or if it is following target_id
            if agent_id not in self.agents_following_targets.values() or self.agents_following_targets[target_id] == agent_id:
                self.agents_following_targets[target_id] = agent_id
                return

    def update_targets_agents(self):
        for target_index in range(len(self.targets)):
            # verify if there is a target already in its index
            if not self.targets[target_index] == Point(-10,-10):
                self.__find_agent_to_target(target_index)

    def agent_has_target(self, agent_id:int):
        for item in self.agents_following_targets:
            if agent_id == self.agents_following_targets[item]: return True
        return False
    
    def agent_target(self, agent_id:int):
        for item in self.agents_following_targets:
            if agent_id == self.agents_following_targets[item]: 
                return item