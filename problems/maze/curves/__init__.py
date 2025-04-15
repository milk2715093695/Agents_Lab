from problems.maze.utils.types import Matrix
from problems.maze.curves.hilbert_curve import generate_hilbert_matrix
from problems.maze.curves.hamilton_curve import generate_hamiltonian_path as gen_hamilton


# 统一接口
def gen_hilbert(m: int, n: int) -> Matrix[int]:
    if m != n:
        raise ValueError(f"错误，{m} 不等于 {n}")
    
    return generate_hilbert_matrix(m)


__all__ = ["gen_hilbert", "gen_hamilton"]