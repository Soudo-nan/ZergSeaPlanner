GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15
SIDEBAR_WIDTH = 5
active_blocks = []
inactive_blocks = []
canvas_list = ["Canvas 1", "Canvas 2", "Canvas 3", "Canvas 4"]
canvas_size_dict = {
    "Canvas 1": (20, 15),
    "Canvas 2": (30, 10),
    "Canvas 3": (10, 20),
    "Canvas 4": (25, 25),
}
canvas_forbidden_dict = {
    "Canvas 1": [
        (2, 10), (3, 3), (4, 4),           # 单个格子
        ((5, 5), (10, 8)),                 # 一个矩形区域，左上(5,5)到右下(10,8)
    ],
    "Canvas 2": [(5, 5), (6, 6)],
    "Canvas 3": [],
    "Canvas 4": [(0, 0), (1, 1)],
}