from utils.FieldPositions import FieldPositions
from utils.Point import Point
import heapq    

class GameManager(FieldPositions):
    def __init__(self):
        super().__init__()
        # target_index, agent_index
        self.targets_its_agents = {}
        # moving_agents_ind, not_relevant
        self.moving_agents_ind = {}
        self.awakened_agents_ind = {}
        for index in range(11):
            self.moving_agents_ind[index] = False

    def __get_agents_dists_to_target(self, target_pos:Point):
        distances = []
        #for agent in range(len(self.blue_agents)):
        for agent in self.awakened_agents_ind:
            # pushes dist and agent_index
            heapq.heappush(distances, (self.blue_agents[agent].dist_to(target_pos), agent))
        return distances

    def __find_agent_to_target(self, target_id:int):
        distances = self.__get_agents_dists_to_target(self.targets[target_id])
        found_agent_not_following = False

        while len(distances) > 0 and not found_agent_not_following: 
            agent_id = heapq.heappop(distances)[1]
            
            if not self.agent_has_target(agent_id) or self.agent_target(agent_id) == target_id:
                found_agent_not_following = True

        if found_agent_not_following: 
            self.targets_its_agents[target_id] = agent_id

        del distances

    def update_targets_agents(self):
        for target_index in range(len(self.targets)):
            # verify if there is a target already in its index
            if not self.targets[target_index] == Point(-10,-10):
                self.__find_agent_to_target(target_index)

    def agent_has_target(self, agent_id:int):
        return (agent_id in self.targets_its_agents.values())

    def agent_target(self, agent_id:int):
        for targets in self.targets_its_agents:
            if self.targets_its_agents[targets] == agent_id:
                return targets