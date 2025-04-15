from problems.maze.utils.types import (Matrix, coordinates)


def rotate_quad(order: int, x: int, y: int, flip_x: int, flip_y: int) -> coordinates:
    """ 旋转/翻转象限 """
    if flip_y == 0:
        if flip_x == 1:
            x = order - 1 - x
            y = order - 1 - y
        x, y = y, x 
    return x, y


def hilbert_index_to_coords(order: int, index: int) -> coordinates:
    """ 将 Hilbert 曲线索引转换为坐标(x, y) """
    x = y = 0
    temp_index = index

    step = 1
    while step < order:
        flip_x = (temp_index // 2) & 1
        flip_y = (temp_index ^ flip_x) & 1

        x, y = rotate_quad(step, x, y, flip_x, flip_y)
        x += step * flip_x
        y += step * flip_y

        temp_index //= 4
        step *= 2

    return x, y


def is_power_of_two(value: int) -> bool:
    """ 验证是否为 2 的幂且至少为 2 """
    return value >= 2 and (value & (value - 1)) == 0


def generate_hilbert_matrix(size: int) -> Matrix[int]:
    """ 生成希尔伯特曲线遍历顺序的二维数组 """
    if not is_power_of_two(size):
        raise ValueError(f"大小错误！{size} 不是 2 的幂")
    
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    
    for index in range(size * size):
        x, y = hilbert_index_to_coords(size, index)
        matrix[x][y] = index + 1
    
    return matrix


if __name__ == "__main__":
    try:
        size = 16
        hilbert_matrix = generate_hilbert_matrix(size)
        
        for row in hilbert_matrix:
            print(row)
            
    except ValueError as error:
        print(error)