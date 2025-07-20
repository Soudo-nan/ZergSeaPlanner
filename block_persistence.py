# block_persistence.py

import json
import os
from gridblock import GridBlock

SAVE_FILE = "saved_blocks.json"


def save_all_canvases(canvas_blocks_dict, filename=SAVE_FILE):
    """
    保存所有 canvas 上的 blocks 到 JSON 文件。

    参数:
        canvas_blocks_dict: dict
            { canvas_name: [block, block, ...] }
        filename: str
            保存的文件名
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
            print(f"[SAVE] Canvas={canvas_name}, row={b.row}, col={b.col},size=({b.width}x{b.height}), tag={b.tag}, label={b.label}")
        data[canvas_name] = block_data

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[SAVE] 保存完成：{filename}")


def load_all_canvases(canvas_manager, filename=SAVE_FILE):
    """
    从 JSON 文件加载所有 blocks，并恢复到 canvas_manager 中。

    参数:
        canvas_manager: CanvasManager 实例
    """
    if not os.path.exists(filename):
        print(f"[LOAD] 文件不存在：{filename}")
        return

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    for canvas_name, block_list in data.items():
        canvas = canvas_manager.canvases.get(canvas_name)
        if not canvas:
            print(f"[LOAD] 未找到 canvas：{canvas_name}，跳过")
            continue

        restored_blocks = []
        for bdata in block_list:
            # 注意参数顺序: col, row, width, height...
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
            print(f"[LOAD] Canvas={canvas_name}, row={bdata['row']}, col={bdata['col']}, size=({bdata['width']}x{bdata['height']}), tag={bdata.get('tag')}, label={bdata.get('label')}")

            restored_blocks.append(block)

        # 恢复后的 blocks 添加到 canvas_manager
        canvas_manager.canvas_blocks[canvas].extend(restored_blocks)

    print(f"[LOAD] 加载完成：{filename}")
