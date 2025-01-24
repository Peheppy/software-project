from utils.FieldPositions import FieldPositions
from utils.Point import Point
import heapq    

class TargetPriorityManager(FieldPositions):
    def __init__(self):
        super().__init__()
        # target_index, agent_index
        self.target_agent = {}

        # awakened_agents_ind, not_relevant
        self.awake_agents_ind = {}

    def __agents_dists_target(self, target_pos:Point):
        distances = []
        for agent_ind in self.awake_agents_ind:
            # pushes dist and agent_index
            heapq.heappush(distances, (self.b_agents[agent_ind].dist_to(target_pos), agent_ind))
        return distances

    def __find_agent_target(self, target_id:int):
        distances = self.__agents_dists_target(self.targets[target_id])
        found_agent_not_following = False
    
        while len(distances) > 0 and not found_agent_not_following: 
            agent_id = heapq.heappop(distances)[1]
            
            # verify if the current agent is following some target
            # or the current agent is following current target
            if not self.agent_has_target(agent_id) or self.agents_target(agent_id) == target_id:
                found_agent_not_following = True

        if found_agent_not_following:
           # sets an agent to current target 
           self.target_agent[target_id] = agent_id

        del distances

    def update_targets_agents(self):

        # verify each target that has been visited
        for target_index in self.target_agent:
            is_close = self.targets[target_index].dist_to(self.b_agents[self.target_agent[target_index]]) < 0.18
            self.v_targets[target_index] = is_close

        for target_index in range(len(self.targets)):

            # remove target that have already been visited from being in the search 
            if self.v_targets[target_index] == True and target_index in self.target_agent:
                self.target_agent.pop(target_index)

            # verify if there is a target already in its index
            if not self.targets[target_index] == Point(-10,-10) and self.v_targets[target_index] == False:
                self.__find_agent_target(target_index)

    def agent_has_target(self, agent_id:int):
        return (agent_id in self.target_agent.values())

    def agents_target(self, agent_id:int):
        for targets in self.target_agent:
            if self.target_agent[targets] == agent_id:
                return targets