from __future__ import annotations
from enum import Enum


class Stone(Enum):
    """棋子类型枚举
    
    表示棋盘上某个位置的状态：空、黑子或白子
    """
    EMPTY = 0   # 空位，没有棋子
    BLACK = 1   # 黑子
    WHITE = 2   # 白子
    

class Color(Enum):
    """玩家颜色枚举
    
    表示当前落子方的颜色，以及提供对手颜色和对应棋子的转换
    """
    BLACK = 1   # 黑方
    WHITE = 2   # 白方
    
    @property
    def opponent(self) -> Color:
        """获取对手的颜色"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE  
    
    @property
    def stone(self) -> Stone:
        """获取当前颜色对应的棋子类型（Stone）"""
        return Stone.BLACK if self == Color.BLACK else Stone.WHITE
    

class Point:
    """棋盘上的坐标点
    
    使用行列索引（row, col）表示棋盘上的一个位置
    """
    def __init__(self, row: int, col: int):
        """初始化坐标点
        
        Args:
            row: 行号（从 0 开始）
            col: 列号（从 0 开始）
        """
        self.row = row
        self.col = col
    
    def __eq__(self, other: object) -> bool:
        """判断两个坐标点是否相等（行和列均相等）"""
        if not isinstance(other, Point):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        """计算坐标点的哈希值，使 Point 可用作字典键或集合元素"""
        return hash((self.row, self.col))
    
    def __repr__(self) -> str:
        """返回坐标点的字符串表示，便于调试"""
        return f"Point(row={self.row}, col={self.col})"
    
    def neighbors(self) -> list[Point]:
        """返回当前点的四个正交方向相邻点（上、下、左、右）"""
        return [
            Point(self.row - 1, self.col),  # 上
            Point(self.row + 1, self.col),  # 下
            Point(self.row, self.col - 1),  # 左
            Point(self.row, self.col + 1)   # 右
        ]