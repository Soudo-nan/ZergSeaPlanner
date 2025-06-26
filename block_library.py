from gridblock import GridBlock
from config import GRID_SIZE
from typing import Dict

template_blocks_by_tag: Dict[str, list] = {}

def create_template_blocks(sidebar, copy_callback):
    """
    Initializes template blocks and adds them to the sidebar.
    """
    def create(col, row, width, height, color, tag, label=""):
        block = GridBlock(None, col, row, width, height, color, tag, label)
        block.tag = tag
        block.description = label
        block.add_callback = lambda b=block: copy_callback(b)
        sidebar.add_block_item(block, label, block.add_callback)

        if tag not in template_blocks_by_tag:
            template_blocks_by_tag[tag] = []
        template_blocks_by_tag[tag].append(block)

    # Add your blocks here
    create(1, 1, 2, 2, "blue", "Terran", "导弹塔")
    create(1, 1, 1, 1, "gray", "Terran", "监视塔")   
    create(1, 1, 2, 4, "red", "Terran", "竖墙")
    create(1, 1, 4, 2, "orange", "Terran", "横墙")    
    create(1, 1, 3, 3, "cyan", "Terran", "地堡")
    create(1, 1, 3, 3, "magenta", "Terran", "兵营")
    create(1, 1, 3, 3, "brown", "Terran", "电磁炮")
    create(1, 1, 2, 2, "yellow", "Protess", "建筑")
    create(1, 1, 1, 3, "purple", "Terran", "二号")
    create(1, 1, 3, 1, "brown", "Zerg", "噩耗")
    sidebar.refresh_tag_list(template_blocks_by_tag)
