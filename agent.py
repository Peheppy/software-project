from utils.ssl.base_agent import BaseAgent

from utils.PathManager import PathManager
from utils.GameManager import GameManager

class MainAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, fm = GameManager()):
        super().__init__(id, yellow)
        self.fm = fm
        self.pm = PathManager()

    def decision(self):
        if len(self.targets) == 0:
            return
        
        self.fm.awakened_agents_ind[self.id] = True
        self.fm.update_pos_blue(self.id, self.pos)
        self.fm.update_targets_agents()

        if self.fm.agent_has_target(self.id) and self.fm.targets[self.fm.agent_target(self.id)] in self.targets:
            target = self.fm.targets[self.fm.agent_target(self.id)]
            self.pm.go_to_target(self.pos, target, self.fm.get_other_agents(self.id), self)
        else:
            self.pm.path.clear()

        return

    def post_decision(self):
        pass