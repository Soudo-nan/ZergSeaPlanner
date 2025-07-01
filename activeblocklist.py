import tkinter as tk

class ActiveBlockList:
    def __init__(self, master, canvas_manager):
        self.canvas_manager = canvas_manager
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.RIGHT, fill="y", padx=5)

        self.label = tk.Label(self.frame, text="当前画布 Blocks", font=("Arial", 12, "bold"))
        self.label.pack(pady=5)

        # 用于显示block列表的frame
        self.blocks_frame = tk.Frame(self.frame)
        self.blocks_frame.pack(fill="both", expand=True)

        # 删除全部按钮
        self.delete_btn = tk.Button(self.frame, text="删除当前画布所有Block", command=self.delete_all_blocks)
        self.delete_btn.pack(pady=10)

        # 监听画布切换
        self.canvas_manager.set_on_switch_callback(self.refresh)

        # 初始刷新
        self.refresh()

    def refresh(self, *args):
        # 清空原有内容
        for widget in self.blocks_frame.winfo_children():
            widget.destroy()
        blocks = self.canvas_manager.get_current_blocks()
        for idx, block in enumerate(blocks):
            row = tk.Frame(self.blocks_frame)
            row.pack(fill="x", pady=1)
            desc = getattr(block, "label", str(block))
            label = tk.Label(row, text=f"{idx+1}. {desc}", anchor="w")
            label.pack(side="left", fill="x", expand=True)
            btn = tk.Button(row, text="删除", width=5, command=lambda b=block: self.delete_block(b))
            btn.pack(side="right")

    def delete_block(self, block):
        canvas = self.canvas_manager.get_current_canvas()
        if canvas and block in self.canvas_manager.canvas_blocks[canvas]:
            # 删除block对应的图形项
            if hasattr(block, "id"):
                canvas.delete(block.id)
            if hasattr(block, "text_id"):
                canvas.delete(block.text_id)
            self.canvas_manager.canvas_blocks[canvas].remove(block)
            self.refresh()

    def delete_all_blocks(self):
        canvas = self.canvas_manager.get_current_canvas()
        if canvas:
            canvas.delete("block")
            self.canvas_manager.canvas_blocks[canvas].clear()
            self.canvas_manager.draw_grid(canvas)
            self.refresh()