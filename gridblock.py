from config import GRID_SIZE

class GridBlock:
    def __init__(self, canvas, col, row, width, height, color, tag=None, label="",
                 outline_color="blue", outline_width=2):
        self.canvas = canvas
        self.col = col
        self.row = row
        self.width = width
        self.height = height
        self.color = color
        self.tag = tag
        self.label = label

        self.outline_color = outline_color
        self.outline_width = outline_width

        self.id = None          # rectangle canvas item ID
        self.text_id = None     # text canvas item ID
        self.selected = False

    def __repr__(self):
        return (f"<GridBlock tag={self.tag} label={self.label} "
                f"pos=({self.col},{self.row}) size=({self.width}x{self.height}) "
                f"color={self.color}>")
    
    def draw(self, canvas=None):
        canvas = canvas or self.canvas
        if not canvas:
            raise ValueError("No canvas to draw on.")

    # Remove old visuals if any (only if drawing on the same canvas)
        if canvas == self.canvas:
            if self.id:
                canvas.delete(self.id)
            if self.text_id:
                canvas.delete(self.text_id)

        x1 = self.col * GRID_SIZE
        y1 = self.row * GRID_SIZE
        x2 = x1 + self.width * GRID_SIZE
        y2 = y1 + self.height * GRID_SIZE

        outline = self.outline_color if self.selected else ""
        width = self.outline_width if self.selected else 1

        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=outline, width=width)
        self.text_id = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.label)

    # Optionally update self.canvas if not already assigned
        if self.canvas is None:
            self.canvas = canvas


    def move_to_grid(self, col, row):
        self.col = max(0, col)
        self.row = max(0, row)
        self.draw()

    def contains_point(self, x, y):
        x1 = self.col * GRID_SIZE
        y1 = self.row * GRID_SIZE
        x2 = x1 + self.width * GRID_SIZE
        y2 = y1 + self.height * GRID_SIZE
        return x1 <= x <= x2 and y1 <= y <= y2

    def collides_with(self, other):
        return not (
            self.col + self.width <= other.col or
            self.col >= other.col + other.width or
            self.row + self.height <= other.row or
            self.row >= other.row + other.height
        )

    @staticmethod
    def is_position_free(col, row, width, height, block_list, exclude_block=None):
        test_block = DummyBlock(col, row, width, height)
        for block in block_list:
            if block is exclude_block:
                continue
            if test_block.collides_with(block):
                return False
        return True

    @staticmethod
    def is_within_bounds(col, row, width, height, max_cols, max_rows):
        return (
            col >= 0 and
            row >= 0 and
            col + width <= max_cols and
            row + height <= max_rows
        )

    def clear(self):
        if self.id:
            self.canvas.delete(self.id)
            self.id = None
        if self.text_id:
            self.canvas.delete(self.text_id)
            self.text_id = None

    def set_selected(self, selected=True):
        self.selected = selected
        self.draw()

class DummyBlock:
    """Helper block for collision checks without canvas."""
    def __init__(self, col, row, width, height):
        self.col = col
        self.row = row
        self.width = width
        self.height = height

    def collides_with(self, other):
        return not (
            self.col + self.width <= other.col or
            self.col >= other.col + other.width or
            self.row + self.height <= other.row or
            self.row >= other.row + other.height
        )