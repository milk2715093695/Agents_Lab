import random
from core import Action, State
from typing import Any, Callable, Dict, List, Set, Tuple
from core.core_bases import Agent, Problem
from core.core_registers import AgentRegistry


@AgentRegistry.register("NormalDFSAgent")
class NormalDFSAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

        self.dfs_stack: List[Tuple[State, Action]] = []
        self.visited: Set[State] = set()

    @classmethod
    def from_config(cls, **config) -> "NormalDFSAgent":
        return cls()
    
    def select_action(self, problem: Problem) -> Action:
        cur_state = problem.get_state()

        if cur_state not in self.visited:
            self._push_into_stack(problem, cur_state)
            self.visited.add(cur_state)

        if self.dfs_stack:
            state, action = self.dfs_stack.pop()
            problem.set_state(state)
            return action

        return None

    def _push_into_stack(self, problem: Problem, state: State) -> None:
        for action in problem.get_legal_actions(state):
            next_state = problem.apply_action_to_state(state, action)
            if next_state not in self.visited:
                self.dfs_stack.append((state, action))



@AgentRegistry.register("NormalDFSAgentOptimized")
class NormalDFSAgentOptimized(Agent):
    def __init__(self) -> None:
        super().__init__()

        self.dfs_stack: List[Tuple[State, Action]] = []
        self.visited: Set[State] = set()
        self.evaluate_func: Callable[[Problem, State, Action], Any] = lambda *_: 0

    @classmethod
    def from_config(cls, **config) -> "NormalDFSAgentOptimized":
        """ 使用配置文件初始化 """
        evaluate_func = config.get("evaluate_func")
        instance = cls()
        
        if evaluate_func:
            instance.evaluate_func = evaluate_func

        return instance
    
    def select_action(self, problem: Problem) -> Action:
        cur_state = problem.get_state()

        if cur_state not in self.visited:
            self._push_into_stack(problem, cur_state)
            self.visited.add(cur_state)

        if self.dfs_stack:
            state, action = self.dfs_stack.pop()
            problem.set_state(state)
            return action

        return None

    def _push_into_stack(self, problem: Problem, state: State) -> None:
        actions = self._sort(list(problem.get_legal_actions(state)), problem)
        for action in actions:
            next_state = problem.apply_action_to_state(state, action)
            if next_state not in self.visited:
                self.dfs_stack.append((state, action))

    def _sort(
        self, actions: List[Action], problem: Problem
    ) -> List[Action]:
        cur_state = problem.get_state()

        def action_score(action: Action) -> tuple[int, float]:
            return self.evaluate_func(problem, cur_state, action)

        return sorted(actions, key=action_score)


@AgentRegistry.register("DFSAgent")
class DFSAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

        self.visited: Dict[State, Set[Action]] = {}
        self.path: List[Tuple[State, Action]] = []

    @classmethod
    def from_config(cls, **config) -> "DFSAgent":
        return cls()

    def select_action(self, problem: Problem) -> Action:
        """ 基于当前问题状态选择动作 """
        cur_state = problem.get_state()

        if cur_state not in self.visited:
            self.visited[cur_state] = set()
        
        valid_actions = problem.get_legal_actions(problem.get_state())
        valid_actions = [
            valid_action for valid_action in valid_actions 
            if (
                valid_action not in self.visited[cur_state]
                and (valid_action != self.path[-1][1].reverse()) if self.path else True
            )
        ]
        random.shuffle(valid_actions)

        if valid_actions:
            chosen_action = valid_actions.pop()

            self.visited[cur_state].add(chosen_action)
            self.path.append((cur_state, chosen_action))

            return chosen_action
        
        if self.path:
            _, last_action = self.path.pop()
            reversed_action = last_action.reverse()
            self.visited[cur_state].add(reversed_action)

            return reversed_action
        
        return None


@AgentRegistry.register("DFSAgentOptimized")
class DFSAgentOptimized(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.all_valid_actions: Dict[State, Set[Action]] = {}
        self.visited: Dict[State, Set[Action]] = {}
        self.path: List[Tuple[State, Action]] = []

    @classmethod
    def from_config(cls, **config) -> "DFSAgentOptimized":
        return cls()

    def select_action(self, problem: Problem) -> Action:
        """ 基于当前问题状态选择动作 """
        cur_state = problem.get_state()

        if cur_state not in self.visited:
            self.visited[cur_state] = set()
        
        valid_actions = problem.get_legal_actions(problem.get_state())
        self.all_valid_actions[cur_state] = [
            valid_action for valid_action in valid_actions
            if valid_action not in self.visited[cur_state]
        ]

        valid_actions = [
            valid_action for valid_action in valid_actions 
            if (
                valid_action not in self.visited[cur_state]
                and (valid_action != self.path[-1][1].reverse()) if self.path else True
            )
        ]
        random.shuffle(valid_actions)

        if valid_actions:
            chosen_action = valid_actions.pop()

            self.visited[cur_state].add(chosen_action)
            self.path.append((cur_state, chosen_action))

            return chosen_action
        
        if self.path:
            self._optimize_path(problem, cur_state)
            
            _, last_action = self.path.pop()
            reversed_action = last_action.reverse()
            self.visited[cur_state].add(reversed_action)

            return reversed_action
        
        return None
    
    def _get_back_path(self) -> List[Tuple[State, Action]]:
        """ 找到从最后一个有效位置出发到当前位置的路径 """
        back_path: List[Tuple[State, Action]] = []
        while True:
            state, action = self.path.pop()
            back_path.append((state, action))
            if self.all_valid_actions[state]:
                break

        return back_path
    
    def _optimize_path(self, problem: Problem, cur_state: State) -> None:
        """ 优化历史路径（只需要保留最后一次经过这个位置的行为即可） """
        back_path = self._get_back_path()

        action_dict: Dict[State, Action] = {}
        back_path.reverse()
        for state, action in back_path:
            action_dict[state] = action
            
        state = back_path[0][0]
        while state != cur_state:
            action = action_dict[state]
            self.path.append((state, action))
            state = problem.apply_action_to_state(state, action)


@AgentRegistry.register("DFSAgentOptimized2")
class DFSAgentOptimized2(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.all_valid_actions: Dict[State, Set[Action]] = {}
        self.visited: Dict[State, Set[Action]] = {}
        self.path: List[Tuple[State, Action]] = []
        self.evaluate_func: Callable[[Problem, State, Action], Any] = lambda *_: 0

    @classmethod
    def from_config(cls, **config) -> "DFSAgentOptimized2":
        """ 使用配置文件初始化 """
        evaluate_func = config.get("evaluate_func")
        instance = cls()
        
        if evaluate_func:
            instance.evaluate_func = evaluate_func

        return instance

    def select_action(self, problem: Problem) -> Action:
        """ 基于当前问题状态选择动作 """
        cur_state = problem.get_state()

        if cur_state not in self.visited:
            self.visited[cur_state] = set()
        
        valid_actions = problem.get_legal_actions(problem.get_state())
        self.all_valid_actions[cur_state] = [
            valid_action for valid_action in valid_actions
            if valid_action not in self.visited[cur_state]
        ]

        valid_actions = [
            valid_action for valid_action in valid_actions 
            if (
                valid_action not in self.visited[cur_state]
                and (valid_action != self.path[-1][1].reverse()) if self.path else True
            )
        ]
        valid_actions = self._sort(valid_actions, problem)

        if valid_actions:
            chosen_action = valid_actions.pop()

            self.visited[cur_state].add(chosen_action)
            self.path.append((cur_state, chosen_action))

            return chosen_action
        
        if self.path:
            self._optimize_path(problem, cur_state)
            
            _, last_action = self.path.pop()
            reversed_action = last_action.reverse()
            self.visited[cur_state].add(reversed_action)

            return reversed_action
        
        return None
    
    def _get_back_path(self) -> List[Tuple[State, Action]]:
        """ 找到从最后一个有效位置出发到当前位置的路径 """
        back_path: List[Tuple[State, Action]] = []
        while True:
            state, action = self.path.pop()
            back_path.append((state, action))
            if self.all_valid_actions[state]:
                break

        return back_path
    
    def _optimize_path(self, problem: Problem, cur_state: State) -> None:
        """ 优化历史路径（只需要保留最后一次经过这个位置的行为即可） """
        back_path = self._get_back_path()

        action_dict: Dict[State, Action] = {}
        back_path.reverse()
        for state, action in back_path:
            action_dict[state] = action
            
        state = back_path[0][0]
        while state != cur_state:
            action = action_dict[state]
            self.path.append((state, action))
            state = problem.apply_action_to_state(state, action)

    def _sort(
        self, actions: List[Action], problem: Problem
    ) -> List[Action]:
        cur_state = problem.get_state()

        def action_score(action: Action) -> tuple[int, float]:
            return self.evaluate_func(problem, cur_state, action)

        return sorted(actions, key=action_score, reverse=True)