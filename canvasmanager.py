import logging
import tkinter as tk
from config import GRID_SIZE, canvas_list, canvas_size_dict, canvas_forbidden_dict

class CanvasManager:
    def __init__(self, parent):
        self.parent = parent
        self.canvases = {}
        self.current_canvas_name = None
        self.canvas_frame = tk.Frame(parent)
        self.canvas_frame.pack(side=tk.LEFT)
        self.canvas_blocks = {}
        self.grid_cache = {}
        self.canvas_sizes = {}  # 新增
        self.forbidden_cells = {}  # 新增

        self.nav_bar = tk.Frame(self.canvas_frame)
        self.nav_bar.pack(side=tk.TOP, anchor="nw", fill=tk.X)

        for name in canvas_list:
            self.add_canvas(name)
            self.create_nav_button(name)

        self.switch_to(canvas_list[0])

    def add_canvas(self, name):
        if name in self.canvases:
            return

        width, height = canvas_size_dict.get(name, (20, 15))
        canvas = tk.Canvas(
            self.canvas_frame,
            width=GRID_SIZE * width,
            height=GRID_SIZE * height,
            bg="white"
        )
        self.canvas_sizes[canvas] = (width, height)
        # 读取config里的不可放置区，支持范围
        forbidden = set()
        for item in canvas_forbidden_dict.get(name, []):
            if isinstance(item, tuple) and len(item) == 2 and all(isinstance(i, tuple) for i in item):
                # 范围 ((x1, y1), (x2, y2))
                (x1, y1), (x2, y2) = item
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        forbidden.add((x, y))
            else:
                # 单个格子
                forbidden.add(item)
        self.forbidden_cells[canvas] = forbidden
        self.draw_grid(canvas, width, height)
        self.canvases[name] = canvas
        self.canvas_blocks[canvas] = []

    def create_nav_button(self, name):
        button = tk.Button(self.nav_bar, text=name, command=lambda: self.switch_to(name))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def switch_to(self, name):
        if self.current_canvas_name:
            self.canvases[self.current_canvas_name].pack_forget()
        self.current_canvas_name = name
        self.canvases[name].pack()

        # Trigger callback if defined
        if hasattr(self, 'on_switch_callback'):
            self.on_switch_callback(name)

    def get_current_canvas(self):
        return self.canvases.get(self.current_canvas_name)

    def get_current_blocks(self):
        canvas = self.get_current_canvas()
        return self.canvas_blocks.get(canvas, [])

    def add_block_to_current_canvas(self, block):
        canvas = self.get_current_canvas()
        if canvas:
            self.canvas_blocks[canvas].append(block)

    def draw_grid(self, canvas, width=None, height=None):
        if canvas in self.grid_cache:
            logging.debug("Grid already drawn for this canvas, skipping redraw.")
            return
        if width is None or height is None:
            width, height = self.canvas_sizes.get(canvas, (20, 15))
        logging.debug("Drawing grid for canvas.")
        for i in range(width + 1):
            canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, GRID_SIZE * height, fill="gray")
        for j in range(height + 1):
            canvas.create_line(0, j * GRID_SIZE, GRID_SIZE * width, j * GRID_SIZE, fill="gray")

        # 高亮不可放置区
        forbidden = self.forbidden_cells.get(canvas, set())
        for (col, row) in forbidden:
            x1 = col * GRID_SIZE
            y1 = row * GRID_SIZE
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            # 半透明红色方块
            canvas.create_rectangle(x1, y1, x2, y2, fill="red", stipple="gray25", outline="")
            # 居中写字
            canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="禁", fill="white", font=("Arial", 10, "bold"))

        self.grid_cache[canvas] = True

    def set_on_switch_callback(self, callback):
        self.on_switch_callback = callback