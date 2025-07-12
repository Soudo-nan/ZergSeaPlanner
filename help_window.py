# help_window.py
import tkinter as tk

def show_help_window():
    help_win = tk.Toplevel()
    help_win.title("操作说明")
    help_win.geometry("400x300")

    help_text = """
操作说明：
- 左键点击并按住方块：拖动方块
- 松开左键：释放方块
- 可以从工具栏或其他面板复制方块到画布
- 禁止区不能放置方块

其他：
- 支持多个画布
- 自动对齐到网格
"""
    label = tk.Label(help_win, text=help_text, justify="left", anchor="nw")
    label.pack(fill="both", expand=True, padx=10, pady=10)
