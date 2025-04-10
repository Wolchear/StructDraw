from abc import ABC, abstractmethod
from typing import Optional

from .chain import RegularLabel, Chain

class _BaseCanvasComponent(ABC):
    def __init__(self):
        self._width = 0
        self._height = 0
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def width(self) -> int:
        return self._width

    @abstractmethod
    def compute_size(self, canvas_width: Optional[int] = None) -> None:
        pass
    
    @abstractmethod
    def draw(self) -> None:
        pass
    
class Title(_BaseCanvasComponent):
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
    
class DrawArea(_BaseCanvasComponent):
    def __init__(self):
        super().__init__()
        self.__chains_storage = []
        
    def add_chain(self, chain: Chain, shape_size, show_amino_code, annotate, split) -> None:
        new_chain = Chain(chain, 'struct', shape_size,show_amino_code,annotate, split)
        self.__chains_storage.append(new_chain)
    
    def compute_size(self) -> None:
        self._height = sum(chain.height for chain in self.__chains_storage)
        self._width = max((chain.width for chain in self.__chains_storage), default=0)
        
    def draw(self, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
    	y_offset = offset 
    	for chain in self.__chains_storage:
    		chain.draw(draw_context, y_offset)
    		y_offset += chain.height
