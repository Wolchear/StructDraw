from abc import ABC, abstractmethod
from .chain import RegularLabel, Chain

class _BaseCanvasComponent(ABC):
    def __init__(self):
        self._width = 0
        self._height = 0
    
    @property
    def height(self) -> int:
        return self._height

    def set_height(self, height: int) -> None:
        self._height = height
    
    @property
    def width(self) -> int:
        return self._width

    def set_width(self, width: int) -> None:
        self._width = width
    
class Title(_BaseCanvasComponent):
    def __init__(self, font:str, font_size:int, text:str, text_position:str = 'right'):
        super().__init__()
        self._height = int(1.5 * font_size)
        
        self.__font_size = font_size
        self.__font = font
        self.__text = text
        
        self.__text_x_offset_multiplier = self._set_x_offset(text_position)
        self.__text_y0 = int(self._height * 0.5 - 0.5 * self.__font_size)
        self.__text_x0 = None
        
    
    def draw_lable(self, draw_context):
        self._count_x0()
        label = RegularLabel(self.__text_x0, self.__text_y0,
                             self.__text, self.__font_size,
                             self.__font)
        label.draw_label(draw_context, 0)
    
    def _count_x0(self) -> None:
    	self.__text_x0 = int( self._width
    	                * self.__text_x_offset_multiplier
    	                - self.__font_size
    	                * 0.3 * len(self.__text))
    
    def _set_x_offset(self, text_position: str):
        text_x_offsets = {'centered': 0.5, 'right': 0.1, 'left': 0.9}
        return text_x_offsets.get(text_position, 0.1)
        
    
    
class DrawArea(_BaseCanvasComponent):
    def __init__(self):
        super().__init__()
        self.__chains_storage = []
        
    def add_chain(self, chain: 'Chain', shape_size, annotate=False, split=None) -> None:
        new_chain = Chain(chain, 'struct', shape_size, annotate, split)
        self.__chains_storage.append(new_chain)
    
    @property
    def chains(self) -> list:
        return self.__chains_storage
       
    def compute_size(self) -> None:
        total_width = 0
        total_height = 0
        for chain in self.__chains_storage:
            if chain.width > total_width:
                total_width = chain.width
            total_height += chain.height
        self._height = total_height
        self._width = total_width
