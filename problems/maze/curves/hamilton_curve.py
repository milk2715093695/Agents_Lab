import random
from problems.maze.utils.types import Matrix

def dfs(grid: Matrix[int], row: int, col: int, step: int, directions: list, path_found: list) -> bool:
    """ 递归搜索哈密尔顿路径 """
    if path_found[0]:
        return True
    
    grid[row][col] = step
    if step == len(grid) * len(grid[0]):
        path_found[0] = True
        return True
    
    shuffled_dirs = random.sample(directions, len(directions))
    for dx, dy in shuffled_dirs:
        nx, ny = row + dx, col + dy
        
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            if dfs(grid, nx, ny, step + 1, directions, path_found):
                return True
    
    if not path_found[0]:
        grid[row][col] = 0
    
    return False

def generate_hamiltonian_path(rows: int, cols: int) -> Matrix[int]:
    """ 生成哈密尔顿路径 """
    if rows * cols >= 50:
        print("警告！哈密尔顿路径生成时间复杂度较高，推荐输入棋盘大小小于 50")
    
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    path_found = [False]
    
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    
    if not dfs(grid, start_x, start_y, 1, directions, path_found):
        for x in range(rows):
            for y in range(cols):
                if dfs(grid, x, y, 1, directions, path_found):
                    break
            if path_found[0]:
                break
    
    return grid

if __name__ == "__main__":
    m, n = 6, 6
    path = generate_hamiltonian_path(m, n)
    for row in path:
        print(row)
