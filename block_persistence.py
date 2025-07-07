# block_persistence.py

import json
import os
from gridblock import GridBlock  # 确保这个路径没错，根据你项目结构调整

SAVE_FILE = "saved_blocks.json"

def save_blocks(active_blocks, filename=SAVE_FILE):
    data = []
    for b in active_blocks:
        data.append({
            "row": b.row,
            "col": b.col,
            "width": b.width,
            "height": b.height,
            "color": b.color,
            "tag": b.tag,
            "label": b.label,
            # 可根据实际需要扩展
        })
    with open(filename, "w") as f:
        json.dump(data, f)

def load_blocks(canvas, filename=SAVE_FILE):
    if not os.path.exists(filename):
        return []
    with open(filename) as f:
        data = json.load(f)
    blocks = []
    for bdata in data:
        block = GridBlock(
            canvas,
            bdata["row"],
            bdata["col"],
            bdata["width"],
            bdata["height"],
            bdata["color"],
            tag=bdata.get("tag"),
            label=bdata.get("label")
        )
        block.draw()
        blocks.append(block)
    return blocks
