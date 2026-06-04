from __future__ import annotations

from core.board import Board
from core.types import Color, Point, Stone
from core.rules import place_stone, is_legal_move, check_win


class GameState:
    """游戏状态管理类

    负责维护一局五子棋的完整状态：
        1、棋盘
        2、当前玩家
        3、是否结束
        4、赢家
        5、历史记录
        6、提供落子、跳过、认输、悔棋操作接口。
    """

    def __init__(self, size: int = 9):
        """初始化一局新游戏

        Args:
            size: 棋盘边长，默认为 9（9×9 棋盘）
        """
        self.board: Board = Board(size)  # 棋盘对象
        self.current_player: Color = Color.BLACK  # 当前落子方，黑方先手
        self.game_over: bool = False  # 游戏是否结束
        self.consecutive_count: int = 0  # 连续跳过次数（双方各跳一次则游戏结束）
        self.move_count: int = 0  # 已下子数（用于统计）
        self.winner: Color | None = None  # 赢家，None 表示无赢家
        # 历史记录，每个元素为 (落子坐标, 当时的连续跳过次数)，
        # 落子坐标在下棋时为 Point，跳过时为 None
        self._history: list[tuple[Point | None, int]] = []

    def play(self, point: Point) -> bool:
        """在指定坐标落子

        执行流程：
            1. 检查游戏是否已结束
            2. 检查落子是否合法
            3. 保存当前状态到历史记录
            4. 在棋盘上放置棋子
            5. 检测是否获胜
            6. 切换玩家

        Args:
            point: 落子的坐标

        Returns:
            True 表示落子成功，False 表示落子失败
        """
        color = self.current_player
        if self.game_over:
            return False  # 游戏已结束，不能继续落子
        if not is_legal_move(self.board, color, point):
            return False  # 非法落子

        self._history.append((point, self.consecutive_count))  # 保存历史
        self.consecutive_count = 0  # 落子重置跳过计数
        self.move_count += 1  # 步数加一
        place_stone(self.board, color, point)  # 放置棋子

        if check_win(self.board, point, color):
            self.game_over = True
            self.winner = color  # 当前方获胜
        self.current_player = color.opponent  # 切换玩家
        return True

    def pass_move(self) -> bool:
        """当前玩家选择停一手

        连续两次跳过则游戏以平局结束

        Returns:
            True 表示跳过成功，False 表示游戏已结束
        """
        if self.game_over:
            return False
        self._history.append((None, self.consecutive_count))  # 记录跳过历史
        self.consecutive_count += 1  # 增加连续跳过计数
        if self.consecutive_count >= 2:
            self.game_over = True  # 双方连续跳过，游戏平局结束
        self.current_player = self.current_player.opponent  # 切换玩家
        return True

    def resign(self) -> None:
        """当前玩家认输，对手获胜"""
        self.winner = self.current_player.opponent  # 对手成为赢家
        self.game_over = True  # 游戏结束

    def regret_move(self) -> bool:
        """悔棋：撤销上一步操作

        从历史记录中弹出最近的一条记录，恢复棋盘和游戏状态
        可以连续悔棋直到回到初始状态

        Returns:
            True 表示悔棋成功，False 表示没有历史记录可撤销
        """
        if not self._history:
            return False  # 没有历史记录，无法悔棋
        last_point, prev_consecutive = self._history.pop()  # 弹出上一步记录
        if last_point is not None:
            # 上一步是落子：清除该位置的棋子
            self.board.place(last_point, Stone.EMPTY)
            self.move_count -= 1
        # 如果是跳过，棋盘不变，只需恢复状态
        self.consecutive_count = prev_consecutive  # 恢复跳过计数
        self.current_player = self.current_player.opponent  # 回退玩家
        self.game_over = False  # 如果之前已结束，重新开启
        self.winner = None  # 清除赢家信息
        return True
