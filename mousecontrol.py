from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from gridblock import GridBlock

# Internal drag target for tracking the currently dragged block
_drag_target = None

def on_press(event, blocks):
    global _drag_target
    _drag_target = None
    event.widget.focus_set()

    for block in reversed(blocks):
        if block.contains_point(event.x, event.y):
            _drag_target = block
            print(f"[DEBUG] Mouse down at ({event.x}, {event.y}), dragging block: {block}")
            break

def on_drag(event, blocks):
    global _drag_target

    if _drag_target:
        grid_x = event.x // GRID_SIZE
        grid_y = event.y // GRID_SIZE

        if (grid_x != _drag_target.col or grid_y != _drag_target.row):
            if (
                GridBlock.is_within_bounds(grid_x, grid_y, _drag_target.width, _drag_target.height, GRID_WIDTH, GRID_HEIGHT)
                and GridBlock.is_position_free(grid_x, grid_y, _drag_target.width, _drag_target.height, blocks, exclude_block=_drag_target)
            ):
                print(f"[DEBUG] Moving block {_drag_target} to ({grid_x}, {grid_y})")
                _drag_target.move_to_grid(grid_x, grid_y)

def on_release(event, blocks):
    global _drag_target
    if _drag_target:
        print(f"[DEBUG] Released block {_drag_target}")
    _drag_target = None

def on_left_click(event, block):
    selected = getattr(block, 'selected', False)
    if selected:
        block.selected = False
        block.canvas.itemconfig(block.id, outline="", width=1)
    else:
        block.selected = True
        block.canvas.itemconfig(block.id, outline="blue", width=2)

def bind_block_events(block, canvas_for_block, sidebar_canvas, left_click_cb, *_):
    canvas_for_block.tag_bind(block.id, "<Button-1>", lambda e, b=block: left_click_cb(e, b))
