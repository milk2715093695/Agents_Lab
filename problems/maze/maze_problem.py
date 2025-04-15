
from math import sqrt
from core.core_bases import Problem
from core.core_registers import ProblemRegistry
from .utils.generate_walls import generate_walls
from .utils.types import coordinates, Direction, Matrix
from typing import Any, Dict, List, Optional, Set, Tuple

@ProblemRegistry.register("MazeProblem")
class MazeProblem(Problem):
    def __init__(
        self, rows: int = 36, cols: int = 36, break_rate: float = 0.05, max_size: int = 40, 
        radius_history: int = 1, radius_cur: int = 2,
        begin: Optional[coordinates] = None, end: Optional[coordinates] = None
    ) -> None:
        # generate walls 保证最外围一定是墙壁，并且迷宫一定是连通的
        self.walls: Matrix[Set[Direction]] = generate_walls(rows, cols, break_rate, max_size)
        self.begin: coordinates = begin or (0, 0)
        self.end: coordinates = end or (rows - 1, cols - 1)
        self.radius_history: int = radius_history
        self.radius_cur: int = radius_cur
        self.count: int = 0
        self.history_path: List[coordinates] = [self.begin]
        self.init_problem_state()

    @classmethod
    def from_config(cls, **config) -> "MazeProblem":
        """使用配置文件初始化 MazeProblem 实例"""
        return cls(
            rows=config.get("rows", 36),
            cols=config.get("cols", 36),
            break_rate=config.get("break_rate", 0.05),
            max_size=config.get("max_size", 40),
            radius_history=config.get("radius_history", 1),
            radius_cur=config.get("radius_cur", 2),
            begin=config.get("begin"),
            end=config.get("end")
        )

    def init_problem_state(self) -> None:
        """  初始化问题状态 """
        self.location = self.begin
        self.goal = self.end
        self.visible = {self.location, self.begin, self.end}
        self.history_path = [self.begin]
        self.count = 0

    def get_start_state(self) -> coordinates:
        """  返回问题的初始状态 """
        return self.begin
    
    def get_end_state(self) -> coordinates:
        return self.end

    def get_state(self) -> coordinates:
        """ 返回当前问题状态的抽象表示 """
        return self.location

    def is_end_state(self, cur_state: coordinates) -> bool:
        return cur_state == self.goal
    
    def get_end_info(self) -> int:
        return self.count
    
    def get_legal_actions(self, state: coordinates) -> Set[Direction]:
        reachable = set()
        for direction in Direction.iter():
            if direction in self.walls[state[0]][state[1]]:
                continue
            reachable.add(direction)

        return reachable
    
    def apply_action(self, action: Direction) -> coordinates:
        """ 应用决策并返回新的状态 """
        if action not in self.get_legal_actions(self.location):
            return self.location
        
        dx, dy = action.delta()
        new_location = (self.location[0] + dx, self.location[1] + dy)
        self.location = new_location
        self.count += 1
        self.history_path.append(new_location)
        self.visible.add(new_location)
        
        return new_location
    
    def apply_action_to_state(self, state: coordinates, action: Direction):
        """ 对特定状态使用决策后的状态 """
        if action not in self.get_legal_actions(state):
            return state
        
        dx, dy = action.delta()
        return (state[0] + dx, state[1] + dy)

    def _get_visible_locations(self) -> Set[coordinates]:
        """ 返回当前状态可见的位置 """
        visible_locations = self.visible.copy()
        radius = self.radius_history
        
        for location in list(visible_locations):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    neighbor = (location[0] + dx, location[1] + dy)
                    if 0 <= neighbor[0] < len(self.walls) and 0 <= neighbor[1] < len(self.walls[0]):
                        visible_locations.add(neighbor)

        radius = self.radius_cur
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                neighbor = (self.location[0] + dx, self.location[1] + dy)
                if 0 <= neighbor[0] < len(self.walls) and 0 <= neighbor[1] < len(self.walls[0]):
                    visible_locations.add(neighbor)
        
        return visible_locations
    
    def _get_walls(self) -> Matrix[Set[Direction]]:
        """ 返回墙壁 """
        return self.walls
    
    def _get_count(self) -> int:
        return self.count
    
    def get_static_render_data(self) -> Dict[str, Any]:
        """ 返回不随时间变化的静态渲染数据（如地图、起点终点等） """
        return {
            "walls": self._get_walls(),
            "begin": self.begin,
            "end": self.end,
            "rows": len(self.walls),
            "cols": len(self.walls[0]),
        }

    def get_dynamic_render_data(self) -> Dict[str, Any]:
        """ 返回动态渲染数据 """
        return {
            "history_path": self.history_path,
            "visible": self._get_visible_locations(),
            "count": self._get_count(),
            "state": self.get_state()
        }
    
    def set_state(self, state: coordinates) -> None:
        self.location = state


def evaluate_func(problem: Problem, state: coordinates, action: Direction) -> Tuple[int, int]:
    start_pos = problem.apply_action_to_state(state, action)
    end_pos = problem.get_end_state()

    manhattan = abs(start_pos[0] - end_pos[0]) + abs(start_pos[0] - end_pos[1])
    euclidean = sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[0] - end_pos[1]) ** 2)

    return (manhattan, euclidean)