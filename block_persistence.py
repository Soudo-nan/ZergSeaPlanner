# block_persistence.py

import json
import os
from gridblock import GridBlock

SAVE_FILE = "saved_blocks.json"

def save_all_canvases(canvas_blocks_dict, filename=SAVE_FILE):
    """
    canvas_blocks_dict: { canvas_name: [block, block, ...] }
    """
    data = {}
    for canvas_name, blocks in canvas_blocks_dict.items():
        block_data = []
        for b in blocks:
            block_data.append({
                "row": b.row,
                "col": b.col,
                "width": b.width,
                "height": b.height,
                "color": b.color,
                "tag": b.tag,
                "label": b.label,
                "radius": b.radius,
                "circle_color": b.circle_color,
            })
        data[canvas_name] = block_data

    with open(filename, "w") as f:
        json.dump(data, f)

def load_all_canvases(canvas_manager, filename=SAVE_FILE):
    """
    canvas_manager: CanvasManager instance
    Will populate canvas_manager.canvas_blocks with blocks
    """
    if not os.path.exists(filename):
        return

    with open(filename) as f:
        data = json.load(f)

    for canvas_name, block_list in data.items():
        canvas = canvas_manager.canvases.get(canvas_name)
        if not canvas:
            continue
        restored_blocks = []
        for bdata in block_list:
            block = GridBlock(
                canvas,
                bdata["col"],
                bdata["row"],
                bdata["width"],
                bdata["height"],
                bdata["color"],
                tag=bdata.get("tag"),
                label=bdata.get("label"),
                radius=bdata.get("radius", 0),
                circle_color=bdata.get("circle_color", "green")
            )
            block.draw(offset=True)
            print(f"Loading block: row={bdata['row']}, col={bdata['col']}. width={bdata['width']}, height={bdata['height']}, tag={bdata.get('tag')}, label={bdata.get('label')}")
            restored_blocks.append(block)

        canvas_manager.canvas_blocks[canvas].extend(restored_blocks)

