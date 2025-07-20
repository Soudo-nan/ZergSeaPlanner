from functools import partial
import tkinter as tk
import logging
from sidelist import SideList
from config import active_blocks
from mousecontrol import on_press, on_drag, on_release
from canvasmanager import CanvasManager
from activeblocklist import ActiveBlockList
from block_persistence import save_all_canvases, load_all_canvases
from help_window import show_help_window
import mousecontrol

# ====== Initialize App ======
root = tk.Tk()
selected_block = None

# ====== Logging Configuration ======
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

# ====== Canvas Manager ======
canvas_manager = CanvasManager(root)
mousecontrol.canvas_manager = canvas_manager    

# ====== Help window button ======
help_button = tk.Button(canvas_manager.nav_bar, text="帮助", command=show_help_window)
help_button.pack(side=tk.RIGHT, padx=5, pady=5)


# ====== Sidebar ======
sidebar = SideList(root, canvas_manager, active_blocks)
active_block_list = ActiveBlockList(root, canvas_manager)

# ====== Load Saved blocks ======
load_all_canvases(canvas_manager)

# 添加加载的所有块到 active_blocks 统一列表中（方便选中、复制等功能）
for blocks in canvas_manager.canvas_blocks.values():
    active_blocks.extend(blocks)

active_block_list.refresh()

# ====== Block Selection ======
def set_selected_block(block):
    global selected_block
    selected_block = block
    logging.debug(f"selected_block set: {block}, canvas={block.canvas}")

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
    logging.info(f"Switched to canvas: {name}")
    bind_events_to_all_canvases()
    canvas_manager.draw_grid(canvas_manager.get_current_canvas())
    active_block_list.refresh()

canvas_manager.set_on_switch_callback(on_canvas_switch)

# ====== Closing Event ======
def on_closing():
    # 创建一个 dict：{canvas_name: blocks}
    canvas_blocks_by_name = {}
    for name, canvas in canvas_manager.canvases.items():
        blocks = canvas_manager.canvas_blocks.get(canvas, [])
        canvas_blocks_by_name[name] = blocks
    save_all_canvases(canvas_blocks_by_name)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# ====== Launch ======
canvas_manager.draw_grid(canvas_manager.get_current_canvas())
root.mainloop()

