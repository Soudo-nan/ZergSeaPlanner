from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from gridblock import GridBlock

# Internal drag target for tracking the currently dragged block
current_dragged_block = None

def on_press(event, blocks):
    global current_dragged_block
    current_dragged_block = None
    event.widget.focus_set()

    for block in reversed(blocks):
        if block.contains_point(event.x, event.y):
            current_dragged_block = block
            print(f"[DEBUG] Mouse down at ({event.x}, {event.y}), dragging block: {block}")
            break

def on_drag(event, blocks):
    global current_dragged_block

    if current_dragged_block:
        grid_x = event.x // GRID_SIZE
        grid_y = event.y // GRID_SIZE

        if (grid_x != current_dragged_block.col or grid_y != current_dragged_block.row):
            if (
                GridBlock.is_within_bounds(grid_x, grid_y, current_dragged_block.width, current_dragged_block.height, GRID_WIDTH, GRID_HEIGHT)
                and GridBlock.is_position_free(grid_x, grid_y, current_dragged_block.width, current_dragged_block.height, blocks, exclude_block=current_dragged_block)
            ):
                print(f"[DEBUG] Moving block {current_dragged_block} to ({grid_x}, {grid_y})")
                current_dragged_block.move_to_grid(grid_x, grid_y)

def on_release(event, blocks):
    global current_dragged_block
    if current_dragged_block:
        print(f"[DEBUG] Released block {current_dragged_block}")
    current_dragged_block = None

def on_left_click(event, block):
    selected = getattr(block, 'selected', False)
    if selected:
        block.selected = False
        block.canvas.itemconfig(block.id, outline="", width=1)
    else:
        block.selected = True
        block.canvas.itemconfig(block.id, outline="blue", width=2)

def bind_block_events(block, canvas_for_block, left_click_cb, *_):
    canvas_for_block.tag_bind(block.id, "<Button-1>", lambda e, b=block: left_click_cb(e, b))