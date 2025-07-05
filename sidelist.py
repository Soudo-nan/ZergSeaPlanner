import logging
import tkinter as tk
from config import GRID_SIZE, SIDEBAR_WIDTH, active_blocks
from gridblock import GridBlock
from mousecontrol import bind_block_events, on_left_click
from block_library import create_template_blocks

class SideList:
    def __init__(self, master, canvas_manager, active_blocks):
        self.canvas_manager = canvas_manager
        self.active_blocks = active_blocks

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.RIGHT, fill="y")

        # Selected tag StringVar
        self.selected_tag = tk.StringVar(value="Choose a tag")

        # Tag menu
        self.tag_menu = tk.OptionMenu(self.frame, self.selected_tag, "Choose a tag", command=self.filter_blocks_by_tag)
        self.tag_menu.pack(pady=5, anchor="n")

        # Scrollable area
        self.scroll_canvas = tk.Canvas(self.frame, width=GRID_SIZE * SIDEBAR_WIDTH, bg="#ddd")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollable_frame = tk.Frame(self.scroll_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.saved_blocks = []

        # Load initial blocks
        create_template_blocks(self, self.copy_to_canvas)

    def copy_to_canvas(self, block):
        if block is None:
            logging.error("No block selected to copy!")
            return
        current_canvas = self.canvas_manager.get_current_canvas()
        if current_canvas is None:
            logging.error("No active canvas to copy to!")
            return

        new_block = GridBlock(
            current_canvas, 1, 1,
            block.width,
            block.height,
            block.color,
            tag=block.tag,
            label=block.label
        )
        new_block.draw()
        self.active_blocks.append(new_block)
        self.canvas_manager.add_block_to_current_canvas(new_block)
        # 刷新 active block list（如果有）
        if hasattr(self.canvas_manager, "on_switch_callback"):
            self.canvas_manager.on_switch_callback(self.canvas_manager.current_canvas_name)
        bind_block_events(new_block, new_block.canvas, new_block.canvas, on_left_click, lambda e, b=new_block: None)
        logging.info(f"Block copied successfully: {new_block}")

    def add_block_item(self, block, description, add_callback):
        item_frame = tk.Frame(self.scrollable_frame, bd=1, relief="solid", padx=5, pady=5)
        item_frame.pack(fill="x", pady=2)

        block_canvas = tk.Canvas(item_frame, width=GRID_SIZE * block.width, height=GRID_SIZE * block.height, bg="white")
        block_canvas.pack()
        block.draw(canvas=block_canvas)

        desc_label = tk.Label(item_frame, text=description, wraplength=GRID_SIZE * SIDEBAR_WIDTH)
        desc_label.pack(pady=2)

        add_btn = tk.Button(item_frame, text="Add to Canvas", command=lambda b=block: add_callback(b))
        add_btn.pack(pady=2)

        if block not in self.saved_blocks:
            self.saved_blocks.append(block)

    def refresh_tag_list(self, tag_dict):
        menu = self.tag_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="Choose a tag", command=lambda: self.filter_blocks_by_tag(""))

        for tag in tag_dict:
            menu.add_command(
                label=tag,
                command=lambda t=tag: (self.selected_tag.set(t), self.filter_blocks_by_tag(t))
            )

    def filter_blocks_by_tag(self, tag):
        logging.debug(f"filter_blocks_by_tag called with tag: {tag}")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        blocks = self.saved_blocks if not tag or tag == "Choose a tag" else [
            b for b in self.saved_blocks if getattr(b, 'tag', None) == tag
        ]

        for block in blocks:
            try:
                desc = getattr(block, 'description', '')
                cb = getattr(block, 'add_callback', lambda b=None: None)
                self.add_block_item(block, desc, cb)
            except Exception as e:
                logging.error(f"Adding block failed: {e}")