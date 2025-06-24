from functools import partial
import tkinter as tk
from sidelist import SideList
from config import active_blocks
from mousecontrol import on_press, on_drag, on_release, on_left_click, bind_block_events
from canvasmanager import CanvasManager

# ====== Initialize App ======
root = tk.Tk()
selected_block = None

# ====== Canvas Manager ======
canvas_manager = CanvasManager(root)  # 修正：移除 canvas_names 参数

# ====== Sidebar ======
sidebar = SideList(root, canvas_manager, active_blocks)

# ====== Block Selection ======
def set_selected_block(block):
    global selected_block
    selected_block = block
    print(f"[DEBUG] selected_block set: {block}, canvas={block.canvas}")

# ====== Canvas Events ======
bound_canvases = set()

def bind_events_to_all_canvases():
    for canvas in canvas_manager.canvases.values():
        if canvas not in bound_canvases:
            canvas.bind("<ButtonPress-1>", lambda event, c=canvas: on_press(event, canvas_manager.canvas_blocks[c]))
            canvas.bind("<B1-Motion>", lambda event, c=canvas: on_drag(event, canvas_manager.canvas_blocks[c]))
            canvas.bind("<ButtonRelease-1>", lambda event, c=canvas: on_release(event, canvas_manager.canvas_blocks[c]))
            bound_canvases.add(canvas)

bind_events_to_all_canvases()

def on_canvas_switch(name):
    print(f"Switched to canvas: {name}")
    bind_events_to_all_canvases()
    canvas_manager.draw_grid(canvas_manager.get_current_canvas())

canvas_manager.set_on_switch_callback(on_canvas_switch)

# ====== Launch ======
canvas_manager.draw_grid(canvas_manager.get_current_canvas())
root.mainloop()
