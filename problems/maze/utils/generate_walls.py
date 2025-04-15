import random
from typing import Optional, Set
from problems.maze.utils.types import (Matrix, Direction)
from problems.maze.curves import (gen_hilbert, gen_hamilton)


def is_valid_position(row: int, col: int, max_row: int, max_col: int) -> bool:
    """ 判断坐标是否在矩阵范围内 """
    return 0 <= row < max_row and 0 <= col < max_col


def sampling_matrix(matrix: Matrix[int]) -> Matrix[Optional[Direction]]:
    """ 生成方向矩阵：为每个格子随机选择一个更高数值的相邻方向 """
    rows, cols = len(matrix), len(matrix[0])
    direction_grid = [["" for _ in range(cols)] for _ in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            valid_dirs = [
                direction for direction in Direction.iter()
                if is_valid_position(row + direction.value[0], col + direction.value[1], rows, cols)
                and matrix[row + direction.value[0]][col + direction.value[1]] > matrix[row][col]
            ]
            direction_grid[row][col] = random.choice(valid_dirs) if valid_dirs else None
    
    return direction_grid


def generate_walls_from_sample_matrix(matrix: Matrix[Optional[Direction]]) -> Matrix[Set[Direction]]:
    """ 用采样好的矩阵生成墙壁 """
    rows, cols = len(matrix), len(matrix[0])
    
    wall_grid = [[set() for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            for direction in Direction.iter():
                d_row, d_col = direction.delta()
                next_row, next_col = row + d_row, col + d_col

                if not is_valid_position(next_row, next_col, rows, cols):
                    wall_grid[row][col].add(direction)
                elif (not matrix[row][col] or matrix[row][col] != direction) and matrix[next_row][next_col] != direction.reverse():
                    wall_grid[row][col].add(direction)

    return wall_grid


def largest_power_of_two(num: int) -> int:
    """ 使用位运算找到比 num 小的最大的 2^n """
    if num < 1:
        return 0
    
    return 1 << (num.bit_length() - 1)


def v2(m: int) -> int:
    """ 计算 m 中包含的因子 2 的个数，即 v₂(m) """
    if m <= 0:
        raise ValueError("m 必须是正整数")

    count = 0
    while m % 2 == 0:
        m //= 2
        count += 1

    return count


def _generate_walls(rows: int, cols: int, max_size: int = 50) -> Matrix[Set[Direction]]:
    length = min(largest_power_of_two(rows), largest_power_of_two(cols))
    result = [[set() for _ in range(cols)] for _ in range(rows)]

    if rows == 1:
        return generate_walls_from_sample_matrix(sampling_matrix([[i for i in range(cols)]]))
    if cols == 1:
        return generate_walls_from_sample_matrix(sampling_matrix([[i] for i in range(rows)]))
    if rows == cols and length == rows:
        return generate_walls_from_sample_matrix(sampling_matrix(gen_hilbert(length, length)))
    if rows * cols < max_size:
        return generate_walls_from_sample_matrix(sampling_matrix(gen_hamilton(rows, cols)))

    if cols >= rows:        
        matrix1 = _generate_walls(rows, length, max_size)
        matrix2 = _generate_walls(rows, cols - length, max_size)

        for row in range(rows):
            result[row][:length] = matrix1[row]
            result[row][length:] = matrix2[row]

        row = random.choice(range(length))
        result[row][length - 1].discard(Direction("RIGHT"))
        result[row][length].discard(Direction("LEFT"))

    if rows > cols:
        matrix1 = _generate_walls(length, cols, max_size)
        matrix2 = _generate_walls(rows - length, cols, max_size)

        for row in range(length):
            result[row][:] = matrix1[row]
        for row in range(length, rows):
            result[row][:] = matrix2[row - length]

        col = random.choice(range(length))
        result[length - 1][col].discard(Direction("DOWN"))
        result[length][col].discard(Direction("UP"))

    return result


def generate_walls(rows: int, cols: int, break_rate: float = 0.1, max_size: int = 50) -> Matrix[Set[Direction]]:
    """ 生成墙壁 """
    if rows <= 0 or cols <= 0:
        raise ValueError("行数和列数必须是正整数")

    walls = _generate_walls(rows, cols, max_size)
    
    for row in range(rows):
        for col in range(cols):
            for direction in list(walls[row][col]):
                if random.random() < break_rate:
                    walls[row][col].discard(direction)
                    next_row, next_col = row + direction.delta()[0], col + direction.delta()[1]
                    if is_valid_position(next_row, next_col, rows, cols):
                        walls[next_row][next_col].discard(direction.reverse()) 

    for row in range(rows):
        walls[row][0].add(Direction("LEFT"))
        walls[row][cols - 1].add(Direction("RIGHT"))

    for col in range(cols):
        walls[0][col].add(Direction("UP"))
        walls[rows - 1][col].add(Direction("DOWN"))

    return walls


if __name__ == "__main__":
    walls_grid = generate_walls(15, 8)
    print(walls_grid)