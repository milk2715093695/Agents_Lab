from pygame import Surface
from typing import Dict, Set
from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def __init__(self, action_str: str) -> None:
        pass
    
    @abstractmethod
    def reverse(self) -> "Action":
        """ 反转动作 """
        pass


class State():
    pass


class Problem(ABC):
    @classmethod
    @abstractmethod
    def from_config(cls, **config) -> "Problem":
        """ 使用配置文件初始化 """
        pass

    @abstractmethod
    def init_problem_state(self) -> None:
        """ 把问题初始化为最初状态 """
        pass

    @abstractmethod
    def get_start_state(self) -> State:
        """ 返回初始状态 """
        pass
    
    @abstractmethod
    def get_end_state(self) -> State:
        """ 返回结束状态 """
        pass

    @abstractmethod
    def get_end_info(self) -> State:
        """ 返回结束状态的信息（游戏结束后打印的信息） """
        pass

    @abstractmethod
    def get_state(self) -> State:
        """ 返回当前问题状态的抽象表示 """
        pass

    @abstractmethod
    def is_end_state(self, cur_state: State) -> bool:
        """ 判断当前状态是否为结束状态 """
        pass
    
    @abstractmethod
    def get_legal_actions(self, state: State) -> Set[Action]:
        """ 返回指定状态下允许的决策列表 """
        pass
    
    @abstractmethod
    def apply_action(self, action: Action) -> State:
        """ 应用决策并返回新的状态 """
        pass

    @abstractmethod
    def apply_action_to_state(self, state: State, action: Action) -> State:
        """ 对特定状态使用决策后的状态 """
        pass

    @abstractmethod
    def get_static_render_data(self) -> Dict[str, State]:
        """ 返回不随时间变化的静态渲染数据 """
        pass

    @abstractmethod
    def get_dynamic_render_data(self) -> Dict[str, State]:
        """ 返回会随状态更新的动态渲染数据 """
        pass


class Agent(ABC):
    @abstractmethod
    def select_action(self, problem: Problem) -> State:
        """ 基于当前问题状态选择动作 """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, **config) -> "Agent":
        """ 使用配置文件初始化 """
        pass


class Renderer(ABC):
    def __init__(self, screen: Surface, problem: Problem, **config) -> None:
        self.problem = problem
        self.config = config
        self.screen = screen
        self.init_renderer(config)

    @abstractmethod
    def render(self, **kwargs) -> None:
        """ 可视化 """
        pass

    @abstractmethod
    def init_renderer(self, config: Dict[str, State]) -> None:
        """ 初始化渲染器 """
        pass