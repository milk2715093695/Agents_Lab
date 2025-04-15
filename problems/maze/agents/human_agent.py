import time
import pygame
from ..utils.types import Direction
from core import Agent, Problem, AgentRegistry

@AgentRegistry.register("MazeHumanAgent")
class MazeHumanAgent(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.last_move_time = 0
        self.move_interval = 0.15

    def select_action(self, problem: Problem) -> Direction:
        """ 持续按键控制，支持方向键与 WASD，并加上移动节流 """

        # 获取当前时间（秒）
        current_time = time.time()

        # 如果冷却时间没到，不移动
        if current_time - self.last_move_time < self.move_interval:
            return None

        keys = pygame.key.get_pressed()

        direction = None
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = Direction("UP")
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = Direction("DOWN")
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = Direction("LEFT")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = Direction("RIGHT")

        # 如果有方向，就更新上次移动时间
        if direction is not None:
            self.last_move_time = current_time

        return direction
    
    @classmethod
    def from_config(cls, **config):
        return