import pygame
from core.core_bases import Renderer
from typing import Any, Dict, Set, Tuple
from core.core_registers import RendererRegistry
from .types import Matrix, coordinates, Direction


draw_rect = pygame.draw.rect


@RendererRegistry.register("MazeRenderer")
class MazeRenderer(Renderer):
    def init_renderer(self, config: Dict[str, Any] = None) -> None:
        """  初始化渲染器 """
        pygame.font.init()
        self.cell_size = config.get("cell_size", 16)
        self.wall_thickness = config.get("wall_thickness", 1)
        self.offset = config.get("offset", 30)
        self.color_config = config.get("color_config", {
            "background": (255, 255, 255),
            "wall": (0, 0, 0),
            "start": (0, 255, 0),
            "end": (255, 0, 0),
            "agent": (0, 0, 255),
            "path": (255, 0, 0),
            "text": (0, 0, 255),
            "invisible": (0, 0, 0)
        })
        self.font_size = config.get("font_size", 24)
        self.render_mask = config.get("render_mask", True)

        self.static_data_dict: Dict[str, Any] = self.problem.get_static_render_data()
        self.dynamic_data_dict: Dict[str, Any] = self.problem.get_dynamic_render_data()

        self.rows = self.static_data_dict["rows"]
        self.cols = self.static_data_dict["cols"]

        self.mask_surface = pygame.Surface((
            (self.rows + 1) * (self.cell_size + self.wall_thickness), 
            (self.cols + 1) * (self.cell_size + self.wall_thickness)
        ), pygame.SRCALPHA)
        self.render()

    def render(self) -> None:
        """ 渲染迷宫 """
        self.screen.fill(self.color_config["background"])
        self._draw_walls()
        self._draw_task()

        self.dynamic_data_dict = self.problem.get_dynamic_render_data()
        self._draw_agent()
        self._draw_counter()
        self._draw_history_path()
        if self.render_mask:
            self._draw_mask()

        pygame.display.flip()

    def _draw_counter(self) -> None:
        font = pygame.font.Font(None, self.font_size)
        text = font.render(
            f"Count: {self.dynamic_data_dict['count']}", 
            True, self.color_config["text"]
        )
        self.screen.blit(text, (self.offset / 2, self.offset / 2))

    def _draw_walls(self) -> None:
        """  绘制迷宫的墙壁 """
        self.walls: Matrix[Set[Direction]] = self.static_data_dict["walls"]

        wall_color = self.color_config["wall"]
        for row in range(self.rows):
            for col in range(self.cols):
                for direction in self.walls[row][col]:
                    draw_rect(self.screen, wall_color, self._get_wall_rect(row, col, direction))

    def _get_wall_rect(self, row: int, col: int, direction: Direction) -> Tuple[int, int, int, int]:
        """ 获取墙壁的矩形区域坐标（左上角 x, y 和宽高 w, h） """
        tot_size = self.cell_size + self.wall_thickness
        cell_x, cell_y = self._cal_position(self.cell_size, self.wall_thickness, row, col)

        if direction == Direction("UP"):
            return (
                cell_x, cell_y, 
                self.cell_size + 2 * self.wall_thickness, self.wall_thickness
            )
        elif direction == Direction("DOWN"):
            return (
                cell_x, cell_y + tot_size, 
                self.cell_size + 2 * self.wall_thickness, self.wall_thickness
            )
        elif direction == Direction("LEFT"):
            return (
                cell_x, cell_y, 
                self.wall_thickness, self.cell_size + 2 * self.wall_thickness
            )
        elif direction == Direction("RIGHT"):
            return (
                cell_x + tot_size, cell_y, 
                self.wall_thickness, self.cell_size + 2 * self.wall_thickness
            )   
        
    def _cal_position(self, cell_size: int, wall_thickness: int, row: int, col: int) -> coordinates:
        """ 计算单元格的坐标（左上角） """
        tot_size = cell_size + wall_thickness
        return (col * tot_size + self.offset, row * tot_size + self.offset)
        
    def _draw_task(self) -> None:
        """ 绘制起点和终点 """
        cell_x, cell_y = self._cal_position(
            self.cell_size, self.wall_thickness, 
            self.static_data_dict["begin"][0], 
            self.static_data_dict["begin"][1]
        )
        draw_rect(
            self.screen, self.color_config["start"], 
            (
                cell_x + self.wall_thickness, cell_y + self.wall_thickness, 
                self.cell_size, self.cell_size
            )
        )

        cell_x, cell_y = self._cal_position(
            self.cell_size, self.wall_thickness, 
            self.static_data_dict["end"][0], 
            self.static_data_dict["end"][1]
        )
        draw_rect(
            self.screen, self.color_config["end"], 
            (
                cell_x + self.wall_thickness, cell_y + self.wall_thickness, 
                self.cell_size, self.cell_size
            )
        )
     
    def _cal_center(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """计算单元格中心坐标（含偏移）"""
        cell_x, cell_y = self._cal_position(self.cell_size, self.wall_thickness, pos[0], pos[1])
        return (
            cell_x + self.cell_size // 2 + self.wall_thickness, 
            cell_y + self.cell_size // 2 + self.wall_thickness
        )
    
    def _draw_mask_at(self, row: int, col: int) -> None:
        tot_size = self.cell_size + self.wall_thickness
        x = col * tot_size
        y = row * tot_size
        draw_rect(
            self.mask_surface, self.color_config["invisible"], 
            (x, y, self.cell_size + 2 * self.wall_thickness, self.cell_size + 2 * self.wall_thickness)
        )

    def _draw_mask(self) -> None:
        self.mask_surface.fill((0, 0, 0, 0))
        self.visible_cells = self.dynamic_data_dict["visible"]
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.visible_cells:
                    self._draw_mask_at(row, col)

        self.screen.blit(self.mask_surface, (self.offset, self.offset))
    
    def _draw_agent(self) -> None:
        """ 绘制智能体 """
        agent_pos = self.dynamic_data_dict["state"]
        cell_x, cell_y = self._cal_center(agent_pos)
        pygame.draw.circle(
            self.screen, self.color_config["agent"], 
            (cell_x, cell_y), self.cell_size // 3
        )

    def _draw_history_path(self) -> None:
        """ 绘制历史路径 """
        history_path = self.dynamic_data_dict["history_path"]
        for i in range(len(history_path) - 1):
            start_pos = self._cal_center(history_path[i])
            end_pos = self._cal_center(history_path[i + 1])
            pygame.draw.line(
                self.screen, self.color_config["path"], 
                start_pos, end_pos, self.wall_thickness
            )
