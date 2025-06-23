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
    create(1, 1, 2, 2, "blue", "Protess", "建筑")
    create(1, 4, 1, 3, "green", "Terran", "一号")
    create(1, 7, 3, 1, "red", "Zerg", "噩耗")

    sidebar.refresh_tag_list(template_blocks_by_tag)
