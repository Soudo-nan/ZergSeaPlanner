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
    create(1, 1, 2, 2, "blue", "人族", "导弹塔", 3, "green")
    create(1, 1, 1, 1, "gray", "人族", "监视塔", 2, "red")
    create(1, 1, 2, 4, "red", "人族", "竖墙", 0, "green")
    create(1, 1, 4, 2, "orange", "人族", "横墙", 0, "green")
    create(1, 1, 3, 3, "cyan", "人族", "地堡", 4, "blue")
    create(1, 1, 3, 3, "magenta", "人族", "兵营", 0, "green")
    create(1, 1, 3, 3, "brown", "人族", "电磁炮", 9, "purple")
    create(1, 1, 5, 5, "yellow", "人族", "钻机", 32, "green")
    create(1, 1, 1, 3, "purple", "人族", "末日武器", 20, "green")
    create(1, 1, 3, 1, "brown", "人族", "AA防空炮", 18, "green")
    create(1, 1, 2, 2, "pink", "人族", "坦克", 5, "green")
    create(1, 1, 2, 2, "lightblue", "人族", "装甲发生器", 3, "green")
    create(1, 1, 5, 5, "lightgreen", "人族", "行星要塞", 4, "green")
    create(1, 1, 2, 2, "lightgray", "人族", "小型兵营", 0, "green")
    create(1, 1, 2, 2, "darkblue", "虫族", "机械虫巢", 6, "green")
    sidebar.refresh_tag_list(template_blocks_by_tag)
