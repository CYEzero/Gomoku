from __future__ import annotations

from core.types import Stone, Color, Point
from core.board import Board


def place_stone(board: Board, color: Color, point: Point) -> None:
    """根据颜色在棋盘的指定位置放置对应的棋子
    
    Args:
        board: 棋盘对象
        color: 落子方的颜色
        point: 落子的坐标
    """
    stone = color.stone     # 将 Color 转换为对应的 Stone 类型
    board.place(point, stone)


def is_legal_move(board: Board, color: Color, point: Point) -> bool:
    """判断在指定位置落子是否合法
    
    检查条件：
        1. 坐标在棋盘范围内
        2. 该位置为空
    
    Args:
        board: 棋盘对象
        color: 落子方的颜色（目前未使用，保留用于扩展规则）
        point: 待检查的坐标
    
    Returns:
        True 表示合法落子，False 表示非法
    """
    if not board.is_on_board(point):
        return False     # 超出棋盘边界
    if board.get(point) != Stone.EMPTY:
        return False     # 该位置已有棋子
    return True


def check_win(board: Board, point: Point, color: Color) -> bool:
    """检查刚刚落子的一方是否获胜
    
    以刚落子的位置为中心，分别检查四个方向（水平、垂直、
    主对角线、副对角线）是否有连续 5 枚同色棋子。
    
    Args:
        board: 棋盘对象
        point: 刚落子的坐标
        color: 落子方的颜色
    
    Returns:
        True 表示该方获胜，False 表示尚未获胜
    """
    target = color.stone        # 需要检查的目标棋子类型
    # 四个需要检查的方向向量：(行偏移, 列偏移)
    directions = [
        (0, 1),   # 水平方向（从左到右）
        (1, 0),   # 垂直方向（从上到下）
        (1, 1),   # 主对角线 ↘（右下）
        (1, -1),  # 副对角线 ↙（左下）
    ]
    for dr, dc in directions:
        count = 1               # 当前棋子本身算 1 个
        # 沿着正方向延伸计数
        r, c = point.row + dr, point.col + dc
        while board.is_on_board(Point(r, c)) and board.grid[r][c] == target:
            count += 1
            r += dr
            c += dc
        # 沿着反方向延伸计数
        r, c = point.row - dr, point.col - dc
        while board.is_on_board(Point(r, c)) and board.grid[r][c] == target:
            count += 1
            r -= dr
            c -= dc
        # 如果某个方向上同色棋子总数 >= 5，则获胜
        if count >= 5:
            return True
    # 四个方向均未连成五子，未获胜
    return False
