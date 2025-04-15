from core import Action
from types import MappingProxyType
from typing import List, Tuple, TypeVar, TypeAlias

# 定义类型变量 T
T = TypeVar("T")

# 定义 Matrix 和 coordinates 的别名
Matrix: TypeAlias = List[List[T]]
coordinates: TypeAlias = Tuple[int, int]

class Direction(Action):
    _members = MappingProxyType({
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
        "UP": (-1, 0)
    })

    def __init__(self, action_str: str) -> None:
        self.name = action_str
        self.value = self._members[action_str]

    @classmethod
    def iter(cls) -> List["Direction"]:
        direction_list = []
        for key in cls._members.keys():
            direction_list.append(cls(key))
        return direction_list

    @classmethod
    def from_tuple(cls, delta: Tuple[int, int]) -> "Direction":
        for direction in cls.iter():
            if direction.value == delta:
                return direction
        raise ValueError(f"无效的增量: {delta}。有效的增量有：{', '.join(str(direction.value) for direction in cls.iter())}。")
    
    def delta(self) -> Tuple[int, int]:
        """ 把方向变成增量 """
        return self.value
    
    def reverse(self) -> "Direction":
        """ 反转方向 """
        return Direction.from_tuple((-self.value[0], -self.value[1]))

    def __repr__(self) -> str:
        direction_str = {
            "UP": '↑', 
            "DOWN": '↓',
            "LEFT": '←',
            "RIGHT": '→'
        }
        return direction_str[self.name]
    
    def __eq__(self, value: "Direction"):
        return value and (self.name == value.name)

    def __hash__(self):
        return hash(self.name)
