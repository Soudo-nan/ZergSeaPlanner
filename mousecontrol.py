from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from gridblock import GridBlock

# Internal drag target for tracking the currently dragged block
_drag_target = None

def on_press(event, blocks):
    """
    On mouse button press, detect if a block is under the mouse and set it as the drag target.
    The blocks list should be ordered topmost last, so we reverse it to check topmost first.
    """
    global _drag_target
    _drag_target = None
    event.widget.focus_set()

    for block in reversed(blocks):  # Check topmost block first
        if block.contains_point(event.x, event.y):
            _drag_target = block
            print(f"[DEBUG] Mouse down at ({event.x}, {event.y}), dragging block: {block}")
            break

def on_drag(event, blocks):
    """
    If a block is being dragged, attempt to move it to the grid cell under the mouse.
    Movement is constrained within bounds and blocks cannot overlap.
    """
    global _drag_target

    if _drag_target:
        grid_x = event.x // GRID_SIZE
        grid_y = event.y // GRID_SIZE

        # Only move if position changes and new position is valid and free
        if (grid_x != _drag_target.col or grid_y != _drag_target.row):
            if (
                GridBlock.is_within_bounds(grid_x, grid_y, _drag_target.width, _drag_target.height, GRID_WIDTH, GRID_HEIGHT)
                and GridBlock.is_position_free(grid_x, grid_y, _drag_target.width, _drag_target.height, blocks, exclude_block=_drag_target)
            ):
                print(f"[DEBUG] Moving block { _drag_target } to ({grid_x}, {grid_y})")
                _drag_target.move_to_grid(grid_x, grid_y)

def on_release(event, blocks):
    """
    Clear the drag target when mouse button is released.
    """
    global _drag_target
    if _drag_target:
        print(f"[DEBUG] Released block {_drag_target}")
    _drag_target = None

def on_right_click(event, block, popup_menu, set_selected_block_cb):
    """
    Handle right-click on a block: select the block and show the popup menu.
    """
    if block is None:
        return
    set_selected_block_cb(block)
    try:
        popup_menu.tk_popup(event.x_root, event.y_root)
    finally:
        popup_menu.grab_release()

def bind_right_click(canvas, block, popup_menu, set_selected_block_cb):
    """
    Bind right-click event on the block's canvas item to show context menu.
    """
    canvas.tag_bind(
        block.id,
        "<Button-3>",
        lambda event: on_right_click(event, block, popup_menu, set_selected_block_cb)
    )

def on_left_click(event, block):
    """
    Toggle selection visual state on the block.
    """
    selected = getattr(block, 'selected', False)
    if selected:
        block.selected = False
        block.canvas.itemconfig(block.id, outline="", width=1)
    else:
        block.selected = True
        block.canvas.itemconfig(block.id, outline="blue", width=2)

def bind_block_events(block, canvas_for_block, sidebar_canvas, left_click_cb, right_click_main_cb, right_click_sidebar_cb):
    """
    Bind left and right click events to the block depending on whether it is in sidebar or main canvas.
    """
    canvas_for_block.tag_bind(block.id, "<Button-1>", lambda e, b=block: left_click_cb(e, b))
    
    if canvas_for_block == sidebar_canvas:
        sidebar_canvas.tag_bind(block.id, "<Button-3>", lambda e, b=block: right_click_sidebar_cb(e, b))
    else:
        canvas_for_block.tag_bind(block.id, "<Button-3>", lambda e, b=block: right_click_main_cb(e, b))
