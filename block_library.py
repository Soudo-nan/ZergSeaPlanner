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
    create(1, 1, 3, 3, "brown", "Terran", "电磁炮", 5, "purple")
    create(1, 1, 2, 2, "yellow", "Protess", "建筑", 0, "green")
    create(1, 1, 1, 3, "purple", "Terran", "二号", 0, "green")
    create(1, 1, 3, 1, "brown", "Zerg", "噩耗", 0, "green")
    sidebar.refresh_tag_list(template_blocks_by_tag)
