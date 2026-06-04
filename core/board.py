from __future__ import annotations
from core.types import Stone, Point


class Board:
    """棋盘类

    维护一个 size × size 的二维网格，记录每个位置上的棋子状态

    提供了对棋盘的基本操作：
        1、放置棋子
        2、查询棋子
        3、判断坐标是否在棋盘内
        4、拷贝棋盘副本
    """

    def __init__(self, size: int):
        """初始化一个 size × size 的空棋盘

        Args:
            size: 棋盘的边长
        """
        self.size: int = size
        # grid[row][col] 表示第 row 行第 col 列的状态，初始全部为空
        self.grid: list[list[Stone]] = [
            [Stone.EMPTY for _ in range(size)] for _ in range(size)
        ]

    def is_on_board(self, point: Point) -> bool:
        """判断给定的坐标点是否在棋盘范围内"""
        return 0 <= point.row < self.size and 0 <= point.col < self.size

    def get(self, point: Point) -> Stone:
        """获取指定坐标点上的棋子类型"""
        return self.grid[point.row][point.col]

    def place(self, point: Point, stone: Stone) -> None:
        """在指定坐标点放置一枚棋子"""
        self.grid[point.row][point.col] = stone

    def copy(self) -> Board:
        """深拷贝当前棋盘，返回一个独立的副本"""
        new_board = Board(self.size)
        for row in range(self.size):
            for col in range(self.size):
                new_board.grid[row][col] = self.grid[row][col]
        return new_board

    def __eq__(self, other: object) -> bool:
        """判断两个棋盘是否相等"""
        if not isinstance(other, Board):
            return NotImplemented
        return self.grid == other.grid

    def __hash__(self) -> int:
        """计算棋盘的哈希值，使 Board 可用作字典键或集合元素"""
        return hash(tuple(tuple(row) for row in self.grid))
