import tkinter as tk

class ActiveBlockList:
    def __init__(self, master, canvas_manager):
        self.canvas_manager = canvas_manager

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.RIGHT, fill="y", padx=5)

        tk.Label(self.frame, text="当前画布 Blocks", font=("Arial", 12, "bold")).pack(pady=5)

        self.blocks_frame = tk.Frame(self.frame)
        self.blocks_frame.pack(fill="both", expand=True)

        tk.Button(
            self.frame,
            text="删除当前画布所有Block",
            command=self.delete_all_blocks
        ).pack(pady=10)

        self.canvas_manager.set_on_switch_callback(self.refresh)
        self.refresh()

    def refresh(self, *args):
        for widget in self.blocks_frame.winfo_children():
            widget.destroy()

        blocks = self.canvas_manager.get_current_blocks()

        # 确保每个 block 都有 original_radius 属性保存原始圆圈大小
        for block in blocks:
            if not hasattr(block, "original_radius"):
                block.original_radius = block.radius

        for idx, block in enumerate(blocks):
            self._add_block_row(idx, block)

    def _add_block_row(self, index, block):
        row = tk.Frame(self.blocks_frame)
        row.pack(fill="x", pady=1)

        desc = getattr(block, "label", str(block))
        tk.Label(row, text=f"{index + 1}. {desc}", anchor="w").pack(side="left", fill="x", expand=True)

        delete_btn = tk.Button(
            row,
            text="删除",
            width=6,
            command=lambda b=block: self.delete_block(b)
        )
        delete_btn.pack(side="right", padx=(2, 0))

        # 判断是否显示切换圆圈按钮，依据 original_radius
        if getattr(block, "original_radius", 0) > 0:
            toggle_btn = tk.Button(row, text="隐藏圆圈", width=10)
            toggle_btn.pack(side="right", padx=(2, 0))

            def toggle_circle():
                if block.radius > 0:
                    block.radius = 0
                    toggle_btn.config(text="显示圆圈")
                else:
                    block.radius = block.original_radius
                    toggle_btn.config(text="隐藏圆圈")
                block.draw()

            toggle_btn.config(command=toggle_circle)

    def delete_block(self, block):
        canvas = self.canvas_manager.get_current_canvas()
        if not canvas:
            return

        block_list = self.canvas_manager.canvas_blocks.get(canvas, [])
        if block in block_list:
            block.clear()
            block_list.remove(block)
            self.refresh()

    def delete_all_blocks(self):
        canvas = self.canvas_manager.get_current_canvas()
        if not canvas:
            return

        for block in self.canvas_manager.canvas_blocks.get(canvas, []):
            block.clear()

        self.canvas_manager.canvas_blocks[canvas].clear()
        self.canvas_manager.draw_grid(canvas)
        self.refresh()
