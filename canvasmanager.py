import tkinter as tk
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class CanvasManager:
    def __init__(self, parent, canvas_names=None):
        self.parent = parent
        self.canvases = {}
        self.current_canvas_name = None
        self.canvas_frame = tk.Frame(parent)
        self.canvas_frame.pack(side=tk.LEFT)
        self.canvas_blocks = {}  # map each canvas -> list of blocks
        self.selector = tk.StringVar()
        self.selector.trace_add("write", self._on_canvas_select)

        self.dropdown = tk.OptionMenu(parent, self.selector, ())
        self.dropdown.pack(side=tk.TOP, pady=5)

        # Use provided names or default to one canvas
        default_names = canvas_names or ["Canvas 1"]
        for name in default_names:
            self.add_canvas(name)

        # Show first canvas by default
        self.switch_to(default_names[0])

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

        # Properly bind the menu command capturing 'name'
        menu = self.dropdown["menu"]
        menu.add_command(label=name, command=lambda n=name: self.selector.set(n))

    def _on_canvas_select(self, *args):
        name = self.selector.get()
        self.switch_to(name)

    def switch_to(self, name):
        if self.current_canvas_name:
            self.canvases[self.current_canvas_name].pack_forget()
        self.current_canvas_name = name
        self.canvases[name].pack()

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
        for i in range(GRID_WIDTH + 1):
            canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, GRID_SIZE * GRID_HEIGHT, fill="gray")
        for j in range(GRID_HEIGHT + 1):
            canvas.create_line(0, j * GRID_SIZE, GRID_SIZE * GRID_WIDTH, j * GRID_SIZE, fill="gray")

    def bind_mouse_events(self, on_press, on_drag, on_release):
        # Fix late binding by capturing blocks list per canvas properly
        for canvas in self.canvases.values():
            blocks_for_canvas = self.canvas_blocks[canvas]
            canvas.bind("<ButtonPress-1>", lambda e, blocks=blocks_for_canvas: on_press(e, blocks))
            canvas.bind("<B1-Motion>", lambda e, blocks=blocks_for_canvas: on_drag(e, blocks))
            canvas.bind("<ButtonRelease-1>", lambda e, blocks=blocks_for_canvas: on_release(e, blocks))

    def set_on_switch_callback(self, callback):
        self.on_switch_callback = callback