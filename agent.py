from utils.ssl.base_agent import BaseAgent

from utils.PathManager import PathManager
from utils.TargetPriorityManager import TargetPriorityManager

class MainAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, tp = TargetPriorityManager()):
        super().__init__(id, yellow)
        self.tp = tp
        self.pm = PathManager()

    def decision(self):
        if len(self.targets) == 0:
            return
        
        # signal for tp, this agent can operate
        self.tp.awake_agents_ind[self.id] = True
        
        # signal position to tp and update targets situation
        self.tp.update_pos_blue(self.id, self.pos)
        self.tp.update_targets_agents()

        # if has target, go to it
        if self.tp.agent_has_target(self.id) and self.tp.targets[self.tp.agents_target(self.id)] in self.targets:
            target = self.tp.targets[self.tp.agents_target(self.id)]
            self.pm.go_to_target(self.pos, target, self.tp.get_other_agents(self.id), self)
        # else just wait
        else:
            self.pm.path.clear()
        return

    def post_decision(self):
        pass