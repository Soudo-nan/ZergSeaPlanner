import tkinter as tk
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, canvas_list

class CanvasManager:
    def __init__(self, parent):
        self.parent = parent
        self.canvases = {}
        self.current_canvas_name = None
        self.canvas_frame = tk.Frame(parent)
        self.canvas_frame.pack(side=tk.LEFT)
        self.canvas_blocks = {}  # map each canvas -> list of blocks
        self.grid_cache = {}  # Cache for grid drawing

        self.nav_bar = tk.Frame(self.canvas_frame)
        self.nav_bar.pack(side=tk.TOP, anchor="nw", fill=tk.X)

        for name in canvas_list:
            self.add_canvas(name)
            self.create_nav_button(name)

        # Show the first canvas by default
        self.switch_to(canvas_list[0])

    def add_canvas(self, name):
        if name in self.canvases:
            return

        canvas = tk.Canvas(
            self.canvas_frame,
            width=GRID_SIZE * GRID_WIDTH,
            height=GRID_SIZE * GRID_HEIGHT,
            bg="white"
        )
        self.draw_grid(canvas)
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

    def draw_grid(self, canvas):
        if canvas in self.grid_cache:
            print("[DEBUG] Grid already drawn for this canvas, skipping redraw.")
            return
        print("[DEBUG] Drawing grid for canvas.")
        for i in range(GRID_WIDTH + 1):
            canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, GRID_SIZE * GRID_HEIGHT, fill="gray")
        for j in range(GRID_HEIGHT + 1):
            canvas.create_line(0, j * GRID_SIZE, GRID_SIZE * GRID_WIDTH, j * GRID_SIZE, fill="gray")
        self.grid_cache[canvas] = True

    def set_on_switch_callback(self, callback):
        self.on_switch_callback = callback