from typing import Dict, List
from .core_bases import Agent, Problem, Renderer


class AgentRegistry:
    """智能体注册器单例类"""
    _instance = None
    _agents: Dict[str, "Agent"] = {}

    def __new__(cls) -> "AgentRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str):
        """注册装饰器"""
        def decorator(agent_class: "Agent"):
            cls._agents[name] = agent_class
            return agent_class
        return decorator

    @classmethod
    def get_agent(cls, name: str) -> "Agent":
        """获取智能体类"""
        return cls._agents.get(name)

    @classmethod
    def list_agents(cls) -> List[str]:
        """列出所有注册的智能体"""
        return list(cls._agents.keys())
    

class ProblemRegistry:
    """问题注册器单例类"""
    _instance = None
    _problems: Dict[str, "Problem"] = {}

    def __new__(cls) -> "ProblemRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str):
        """注册装饰器"""
        def decorator(problem_class: "Problem"):
            cls._problems[name] = problem_class
            return problem_class
        return decorator

    @classmethod
    def get_problem(cls, name: str) -> "Problem":
        """获取问题类"""
        return cls._problems.get(name)

    @classmethod
    def list_problems(cls) -> List[str]:
        """列出所有注册的问题"""
        return list(cls._problems.keys())
    

class RendererRegistry:
    """渲染器注册器单例类"""
    _instance = None
    _renderers: Dict[str, "Renderer"] = {}

    def __new__(cls) -> "RendererRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str):
        """注册装饰器"""
        def decorator(renderer_class: "Renderer"):
            cls._renderers[name] = renderer_class
            return renderer_class
        return decorator

    @classmethod
    def get_renderer(cls, name: str) -> "Renderer":
        """获取渲染器类"""
        return cls._renderers.get(name)

    @classmethod
    def list_renderers(cls) -> List[str]:
        """列出所有注册的渲染器"""
        return list(cls._renderers.keys())
