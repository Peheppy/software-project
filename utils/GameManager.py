from utils.FieldPositions import FieldPositions
from utils.Point import Point
import heapq    

class GameManager(FieldPositions):
    def __init__(self):
        super().__init__()
        # agent_index, target_index
        self.agents_following_targets = {}
        # awakened_agents_ind, not_relevant
        self.awakened_agents_ind = {}
        self.idle_positions = [Point(5,10),Point(15,10),Point(25,10),
                               Point(35,10),Point(5,30),Point(5,50),
                               Point(15,30),Point(15,50),Point(25,30),
                               Point(25,50),Point(35,30)]

    def __get_agents_dists_to_target(self, target_pos:Point):
        distances = []
        for agent in self.awakened_agents_ind:
            # pushes dist and agent_index
            heapq.heappush(distances, (self.blue_agents[agent].dist_to(target_pos), agent))
        return distances

    def __find_agent_to_target(self, target_id:int):
        distances = self.__get_agents_dists_to_target(self.targets[target_id])
        found_agent_not_following = False

        while len(distances) > 0 and not found_agent_not_following: 
            agent_id = heapq.heappop(distances)[1]
            
            if not self.agent_has_target(agent_id):
                found_agent_not_following = True

        if found_agent_not_following: 
            self.agents_following_targets[agent_id] = target_id

    def update_targets_agents(self):
        for target_index in range(len(self.targets)):
            # verify if there is a target already in its index
            if not self.targets[target_index] == Point(-10,-10):
                self.__find_agent_to_target(target_index)

    def agent_has_target(self, agent_id:int):
        return (agent_id in self.agents_following_targets)

    def agent_target(self, agent_id:int):
        return self.agents_following_targets[agent_id]