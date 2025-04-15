import random
from core import Agent, Problem, Action, AgentRegistry


@AgentRegistry.register("RandomAgent")
class RandomAgent(Agent):
    def select_action(self, problem: Problem) -> Action:
        """ 基于当前问题状态选择动作 """
        return random.choice(list(problem.get_legal_actions(problem.get_state())))
    
    @classmethod
    def from_config(cls, **config):
        return