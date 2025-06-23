import tkinter as tk
from config import GRID_SIZE, GRID_HEIGHT, GRID_WIDTH, SIDEBAR_WIDTH

class SideList:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.RIGHT, fill="y")

        # Selected tag StringVar with initial prompt
        self.selected_tag = tk.StringVar(value="Choose a tag")

        # OptionMenu with callback to filter blocks on tag selection
        self.tag_menu = tk.OptionMenu(self.frame, self.selected_tag, "Choose a tag", command=self.filter_blocks_by_tag)
        self.tag_menu.pack(pady=5, anchor="n")

        # Scrollable canvas area to list block items
        self.scroll_canvas = tk.Canvas(self.frame, width=GRID_SIZE * SIDEBAR_WIDTH, bg="#ddd")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollable_frame = tk.Frame(self.scroll_canvas)

        # Connect scrollbar and canvas scrolling region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.scroll_window = self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.saved_blocks = []  # List of all blocks added to sidebar

    def add_block_item(self, block, description, add_callback):
        """
        Add a block item to the sidebar scrollable list, showing its preview, label, and add button.
        """
        item_frame = tk.Frame(self.scrollable_frame, bd=1, relief="solid", padx=5, pady=5)
        item_frame.pack(fill="x", pady=2)

        # Canvas for block preview
        block_canvas = tk.Canvas(item_frame, width=GRID_SIZE * block.width, height=GRID_SIZE * block.height, bg="white")
        block_canvas.pack()
        block.draw(canvas=block_canvas)

        # Label for description
        desc_label = tk.Label(item_frame, text=description, wraplength=GRID_SIZE * SIDEBAR_WIDTH)
        desc_label.pack(pady=2)

        # Button to add block to main canvas
        add_btn = tk.Button(item_frame, text="Add to Canvas", command=lambda b=block, cb=add_callback: cb(b))
        add_btn.pack(pady=2)

        # Save block reference for filtering
        if block not in self.saved_blocks:
            self.saved_blocks.append(block)

    def refresh_tag_list(self, tag_dict):
        """
        Refresh the dropdown menu with tags from the provided tag dictionary.
        Selecting a tag filters the blocks shown in the sidebar.
        """
        menu = self.tag_menu["menu"]
        menu.delete(0, "end")

        # Option to reset filter
        menu.add_command(label="Choose a tag", command=lambda: self.filter_blocks_by_tag(""))

        for tag in tag_dict:
            menu.add_command(
                label=tag,
                command=lambda t=tag: (self.selected_tag.set(t), self.filter_blocks_by_tag(t))
            )

    def filter_blocks_by_tag(self, tag):
        print(f"[DEBUG] filter_blocks_by_tag called with tag: {tag}")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not tag or tag == "Choose a tag":
            # Show all blocks
            for block in self.saved_blocks:
                try:
                    self.add_block_item(block, getattr(block, 'description', ''), getattr(block, 'add_callback', lambda b=None: None))
                except Exception as e:
                    print(f"[ERROR] Adding block failed: {e}")
        else:
            # Show blocks matching tag
            for block in self.saved_blocks:
                try:
                    if getattr(block, 'tag', None) == tag:
                        self.add_block_item(block, getattr(block, 'description', ''), getattr(block, 'add_callback', lambda b=None: None))
                except Exception as e:
                    print(f"[ERROR] Adding block failed: {e}")
