import re
from core.types import Point, Stone
from core.state import GameState


def praise_input(text: str) -> Point | str | None:
    """解析玩家输入的指令或坐标

    支持的命令：
        - "pass"   : 跳过当前回合
        - "resign" : 认输
        - "regret" : 悔棋
        - 坐标格式 : 如 "3,4" 或 "(3,4)" 或 "3，4"（支持中文逗号）

    Args:
        text: 玩家输入的原始字符串

    Returns:
        - 如果识别为命令，返回对应的命令字符串
        - 如果识别为坐标，返回 Point 对象
        - 无法识别时返回 None
    """
    text = text.strip().lower()
    if text == "pass":
        return "pass"
    if text == "resign":
        return "resign"
    if text == "regret":
        return "regret"
    # 匹配坐标
    m = re.match(r"\(?\s*(\d+)\s*[,，]\s*(\d+)\s*\)?", text)
    if m:
        return Point(int(m.group(1)), int(m.group(2)))
    return None


def print_board(game: GameState) -> None:
    """在控制台打印当前棋盘状态

    用数字表示棋子：
        - 0 : 空位
        - 1 : 黑子
        - 2 : 白子

    Args:
        game: 当前游戏状态
    """
    board = game.board
    for r in range(board.size):
        row = []
        for c in range(board.size):
            stone = board.grid[r][c]
            if stone == Stone.EMPTY:
                row.append("0")
            elif stone == Stone.BLACK:
                row.append("1")
            else:
                row.append("2")
        print(row)


def main() -> None:
    """游戏主循环

    流程：
        1. 初始化游戏状态
        2. 进入循环，每轮提示当前玩家输入
        3. 解析输入，执行对应操作（落子/跳过/认输/悔棋）
        4. 打印更新后的棋盘
        5. 检查游戏是否结束，显示获胜信息
        6. 游戏结束后退出
    """
    game = GameState()
    print("五子棋游戏开始！")
    print(
        "请输入坐标 (row col) 来下棋，输入 'pass' 跳过，输入 'resign' 认输，输入 'regret' 悔棋。"
    )
    while not game.game_over:
        print(f"当前玩家: {game.current_player.name}")
        inp = input("> ").strip()
        if not inp:
            continue  # 空输入，重新提示

        result = praise_input(inp)
        if result == "pass":  # 停一手
            game.pass_move()
            print(f"{game.current_player.opponent.name} 选择了跳过。")
        elif result == "resign":  # 认输
            game.resign()
            print(f"{game.current_player.name} 选择了认输。")
        elif result == "regret":  # 悔棋
            game.regret_move()
            print("悔棋成功。")
        elif isinstance(result, Point):  # 落子
            if game.play(result):
                print(f"{game.current_player.opponent.name} 在 {result} 下了一子。")
            else:
                print("非法的落子，请重新输入。")
                continue  # 重新输入
        else:
            print("无法识别的输入，请重新输入。")
            continue  # 重新输入

        print_board(game)  # 打印棋盘
        if game.game_over and game.winner is not None:
            print(f"{game.winner.name} 获胜！")
        print()

    print("游戏结束！")


if __name__ == "__main__":
    main()
