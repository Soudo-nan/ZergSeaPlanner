import logging
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from gridblock import GridBlock
from canvasmanager import CanvasManager

current_dragged_block = None
canvas_manager = None  # 由 main.py 注入

# 新增：记录鼠标在 block 内的偏移
drag_offset_x = 0
drag_offset_y = 0

def on_press(event, blocks):
    global current_dragged_block, drag_offset_x, drag_offset_y
    current_dragged_block = None
    event.widget.focus_set()

    canvas = event.widget
    # 转换为画布坐标
    canvas_x = canvas.canvasx(event.x)
    canvas_y = canvas.canvasy(event.y)

    for block in reversed(blocks):
        if block.contains_point(canvas_x, canvas_y):
            current_dragged_block = block
            block_left = block.col * GRID_SIZE
            block_top = block.row * GRID_SIZE
            drag_offset_x = canvas_x - block_left
            drag_offset_y = canvas_y - block_top
            logging.debug(f"Mouse down at ({canvas_x}, {canvas_y}), dragging block: {block}, offset=({drag_offset_x},{drag_offset_y})")
            break

def on_drag(event, blocks):
    global current_dragged_block, drag_offset_x, drag_offset_y

    if current_dragged_block:
        canvas = event.widget
        # 转换为画布坐标
        canvas_x = canvas.canvasx(event.x)
        canvas_y = canvas.canvasy(event.y)

        new_left = canvas_x - drag_offset_x
        new_top = canvas_y - drag_offset_y
        grid_x = int(new_left // GRID_SIZE)
        grid_y = int(new_top // GRID_SIZE)

        if canvas_manager and canvas in canvas_manager.canvas_sizes:
            width, height = canvas_manager.canvas_sizes[canvas]
            forbidden_cells = canvas_manager.forbidden_cells.get(canvas, set())
        else:
            width, height = GRID_WIDTH, GRID_HEIGHT
            forbidden_cells = set()

        def is_in_forbidden_area(x, y, w, h, forbidden):
            for dx in range(w):
                for dy in range(h):
                    if (x + dx, y + dy) in forbidden:
                        return True
            return False

        if (grid_x != current_dragged_block.col or grid_y != current_dragged_block.row):
            if (
                GridBlock.is_within_bounds(
                    grid_x, grid_y,
                    current_dragged_block.width, current_dragged_block.height,
                    width, height
                )
                and GridBlock.is_position_free(
                    grid_x, grid_y,
                    current_dragged_block.width, current_dragged_block.height,
                    blocks, exclude_block=current_dragged_block
                )
                and not is_in_forbidden_area(
                    grid_x, grid_y,
                    current_dragged_block.width, current_dragged_block.height,
                    forbidden_cells
                )
            ):
                logging.debug(f"Moving block {current_dragged_block} to ({grid_x}, {grid_y})")
                current_dragged_block.move_to_grid(grid_x, grid_y)

def on_release(event, blocks):
    global current_dragged_block
    current_dragged_block = None
