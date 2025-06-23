import tkinter as tk
from sidelist import SideList
from gridblock import GridBlock
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from mousecontrol import on_press, on_drag, on_release, on_left_click, bind_block_events
from canvasmanager import CanvasManager
from block_library import create_template_blocks

# ====== Initialize App ======
root = tk.Tk()
template_blocks_by_tag = {}
selected_block = None

# ====== Sidebar and Canvas Manager ======
sidebar = SideList(root)
canvas_manager = CanvasManager(root, canvas_names=["Canvas 1", "Canvas 2", "Canvas 3", "Canvas 4"])

# ====== Trackers ======
active_blocks = []

def set_selected_block(block):
    global selected_block
    selected_block = block
    print(f"[DEBUG] selected_block set: {block}, canvas={block.canvas}")

def get_blocks_for_canvas(canvas):
    return [block for block in active_blocks if block.canvas == canvas]

# ====== Event Handlers ======
def copy_template_block_to_active_canvas(template_block):
    if template_block is None:
        print("Error: No block selected to copy!")
        return
    current_canvas = canvas_manager.get_current_canvas()
    if current_canvas is None:
        print("Error: No active canvas to copy to!")
        return
    print(f"Copying block: {template_block}")
    new_block = GridBlock(
        current_canvas, 1, 1,
        template_block.width,
        template_block.height,
        template_block.color,
        tag=template_block.tag,
        label=template_block.label
    )
    new_block.draw()
    active_blocks.append(new_block)
    canvas_manager.add_block_to_current_canvas(new_block)
    print(f"Block copied successfully: {new_block}")

def bind_events_to_all_canvases():
    for canvas in canvas_manager.canvases.values():
        canvas.unbind("<ButtonPress-1>")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")

        canvas.bind("<ButtonPress-1>", lambda event, c=canvas: on_press(event, canvas_manager.canvas_blocks[c]))
        canvas.bind("<B1-Motion>", lambda event, c=canvas: on_drag(event, canvas_manager.canvas_blocks[c]))
        canvas.bind("<ButtonRelease-1>", lambda event, c=canvas: on_release(event, canvas_manager.canvas_blocks[c]))

# ====== Bind events and canvas setup ======
bind_events_to_all_canvases()

def on_canvas_switch(name):
    print(f"Switched to canvas: {name}")
    bind_events_to_all_canvases()
    canvas_manager._draw_grid(canvas_manager.get_current_canvas())

canvas_manager.set_on_switch_callback(on_canvas_switch)

canvas_manager._draw_grid(canvas_manager.get_current_canvas())
create_template_blocks(sidebar, copy_template_block_to_active_canvas)

root.mainloop()
