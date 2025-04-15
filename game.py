import random
import pygame
import agents
from typing import Any, List 
from problems import evaluate_func
from core import (
    ProblemRegistry, RendererRegistry, AgentRegistry,
    Problem, Renderer, Agent
)


assert(agents)


def select(array: List[Any], prompt: str) -> Any:
    while True:
        for idx, value in enumerate(array):
            print(f"{idx + 1}. {value}")
        
        idx_str = input(prompt)
        print()

        try:
            idx = int(idx_str)
            if idx < 1 or idx > len(array):
                raise ValueError("输入范围错误！")
        except ValueError:
            print("请输入合法的整数编号！")
            continue

        return array[idx - 1]
    

def main() -> None:
    problem_str: str = select(ProblemRegistry.list_problems(), "请输入问题编号 >>> ")
    renderer_str: str = problem_str.replace("Problem", "Renderer")
    agent_str: str = select(AgentRegistry.list_agents(), "请输入智能体编号 >>> ")

    fps = int(input("请输入 FPS >>> ")) if "HumanAgent" not in agent_str else 50

    SelectedProblem = ProblemRegistry.get_problem(problem_str)
    SelectedRenderer = RendererRegistry.get_renderer(renderer_str)
    SelectedAgent = AgentRegistry.get_agent(agent_str)

    screen = pygame.display.set_mode((800, 800))
    problem: Problem = SelectedProblem.from_config()
    renderer: Renderer = SelectedRenderer(screen, problem)
    agent = SelectedAgent.from_config(evaluate_func=evaluate_func)

    main_loop(problem, renderer, agent, fps = fps)

    pygame.quit()


def main_loop(problem: Problem, renderer: Renderer, agent: Agent, fps) -> None:
    clock = pygame.time.Clock()
    problem.init_problem_state()
    renderer.render()
    random.seed(5)

    running = True
    while running:
        if problem.is_end_state(problem.get_state()):
            end_info = problem.get_end_info()
            print(end_info)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = agent.select_action(problem)
        problem.apply_action(action)
        renderer.render()
        clock.tick(fps)


if __name__ == "__main__":
    main()