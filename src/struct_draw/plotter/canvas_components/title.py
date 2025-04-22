from .base_component import BaseCanvasComponent
from struct_draw.plotter.small_units.label import RegularLabel

class Title(BaseCanvasComponent):
    def __init__(self):
        super().__init__()
        self._label = None
        self._text_position = None
    
    def add_label(self, font: str, font_size: int, text: str, text_position: str = 'left') -> None:
        self._label = RegularLabel(text, font_size, font)
        self._text_position = text_position
        
    def draw(self, draw_context) -> None:
        if self._label is not None:
            x_0 = self._count_x0()
            y_0 = self._count_y_0()
            self._label.draw(x_0, y_0, draw_context)
    
    def _count_x0(self) -> int:
        text_x_offsets = {'left': 0.1, 'centered': 0.5, 'right': 0.9}
        if self._text_position == 'right':
            return int((self.width - self._label.width) * text_x_offsets['right'])
        return int(self.width * text_x_offsets.get(self._text_position, 0.1))
    
    def _count_y_0(self) -> int:
        return int(self._label.height * 0.25)
    
    def compute_size(self, canvas_width: int) -> None:
        self._width = canvas_width
        if self._label is not None:
            self._height = 2 * self._label.height
