GRID_SIZE = 15
GRID_WIDTH = 20
GRID_HEIGHT = 15
SIDEBAR_WIDTH = 5
active_blocks = []
inactive_blocks = []
canvas_list = ["上", "下", "左", "右"]
canvas_size_dict = {
    "上": (50, 50),
    "下": (50, 50),
    "左": (50, 50),
    "右": (50, 50),
}
canvas_forbidden_dict = {
    "上": [
        (2, 10), (3, 3), (4, 4),           # 单个格子
        ((5, 5), (10, 8)),                 # 一个矩形区域，左上(5,5)到右下(10,8)
    ],
    "下": [(5, 5), (6, 6)],
    "左": [],
    "右": [(0, 0), (1, 1)],
}