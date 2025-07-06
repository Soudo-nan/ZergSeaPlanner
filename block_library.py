import logging
from gridblock import GridBlock
from config import GRID_SIZE
from typing import Dict

template_blocks_by_tag: Dict[str, list] = {}

def create_template_blocks(sidebar, copy_callback):
    """
    Initializes template blocks and adds them to the sidebar.
    """
    def create(col, row, width, height, color, tag, label="", radius=0, circle_color="green"):
        block = GridBlock(
        canvas=None,
        col=col,
        row=row,
        width=width,
        height=height,
        color=color,
        tag=tag,
        label=label,
        radius=radius,
        circle_color=circle_color
    )
        block.tag = tag
        block.description = label
        block.add_callback = lambda b=block: copy_callback(b)
        sidebar.add_block_item(block, label, block.add_callback)

        if tag not in template_blocks_by_tag:
            template_blocks_by_tag[tag] = []
        template_blocks_by_tag[tag].append(block)

    # 最后两个参数为半径（单位为格）和圆的颜色
    create(1, 1, 2, 2, "blue", "Terran", "导弹塔", 3, "green")
    create(1, 1, 1, 1, "gray", "Terran", "监视塔", 2, "red")
    create(1, 1, 2, 4, "red", "Terran", "竖墙", 0, "green")
    create(1, 1, 4, 2, "orange", "Terran", "横墙", 0, "green")
    create(1, 1, 3, 3, "cyan", "Terran", "地堡", 4, "blue")
    create(1, 1, 3, 3, "magenta", "Terran", "兵营", 0, "green")
    create(1, 1, 3, 3, "brown", "Terran", "电磁炮", 9, "purple")
    create(1, 1, 2, 2, "yellow", "Terran", "建筑", 32, "green")
    create(1, 1, 1, 3, "purple", "Terran", "二号", 20, "green")
    create(1, 1, 3, 1, "brown", "Terran", "AA防空炮", 18, "green")
    create(1, 1, 2, 2, "pink", "Terran", "小型导弹塔", 5, "green")
    create(1, 1, 2, 2, "lightblue", "Terran", "小型监视塔", 3, "green")
    create(1, 1, 2, 2, "lightgreen", "Terran", "小型地堡", 4, "green")
    create(1, 1, 2, 2, "lightgray", "Terran", "小型兵营", 0, "green")
    create(1, 1, 2, 2, "darkblue", "Zerg", "虫巢", 6, "green")
    create(1, 1, 2, 2, "darkred", "Zerg", "虫穴", 4, "green")
    create(1, 1, 2, 2, "darkgreen", "Zerg", "虫塔", 8, "green")
    create(1, 1, 2, 2, "darkcyan", "Zerg", "虫巢", 10, "green")
    create(1, 1, 2, 2, "darkmagenta", "Zerg", "虫巢", 12, "green")
    create(1, 1, 2, 2, "darkyellow", "Zerg", "虫巢", 14, "green")
    create(1, 1, 2, 2, "darkgray", "Zerg", "虫巢", 16, "green")
    create(1, 1, 2, 2, "darkpink", "Zerg", "虫巢", 18, "green")
    create(1, 1, 2, 2, "darklightblue", "Zerg", "虫巢", 20, "green")
    create(1, 1, 2, 2, "darklightgreen", "Zerg", "虫巢", 22, "green")
    create(1, 1, 2, 2, "darklightgray", "Zerg", "虫巢", 24, "green")
    create(1, 1, 2, 2, "darkbrown", "Zerg", "虫巢", 26, "green")
    create(1, 1, 2, 2, "darkorange", "Zerg", "虫巢", 28, "green")
    sidebar.refresh_tag_list(template_blocks_by_tag)
