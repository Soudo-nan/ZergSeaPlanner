import logging
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from gridblock import GridBlock
from canvasmanager import CanvasManager

# Internal drag target for tracking the currently dragged block
current_dragged_block = None
canvas_manager = None  # 由 main.py 注入

def on_press(event, blocks):
    global current_dragged_block
    current_dragged_block = None
    event.widget.focus_set()

    for block in reversed(blocks):
        if block.contains_point(event.x, event.y):
            current_dragged_block = block
            logging.debug(f"Mouse down at ({event.x}, {event.y}), dragging block: {block}")
            break

def on_drag(event, blocks):
    global current_dragged_block

    if current_dragged_block:
        grid_x = event.x // GRID_SIZE
        grid_y = event.y // GRID_SIZE

        canvas = event.widget
        if canvas_manager and canvas in canvas_manager.canvas_sizes:
            width, height = canvas_manager.canvas_sizes[canvas]
            forbidden_cells = canvas_manager.forbidden_cells.get(canvas, set())
        else:
            width, height = GRID_WIDTH, GRID_HEIGHT
            forbidden_cells = set()

        # 检查是否有重叠到不可放置区
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
    if current_dragged_block:
        logging.debug(f"Released block {current_dragged_block}")
    current_dragged_block = None
