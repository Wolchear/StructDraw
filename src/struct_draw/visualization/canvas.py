from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from .shapes import RegularLabel

class Canvas:
    def __init__(self, background_color: str):
        self.__background_color = background_color
        self.__title_obj = None
        self.__legend_obj = None
        self.__draw_area_obj = _DrawArea()
        self.__height = 0
        self.__width = 0
        self.__title_ends = 0
        	
    def add_chain(self, chain: 'Chain') -> None:
        self.__draw_area_obj.add_chain(chain)
        
    def add_title(self, font:str, font_size:int, text:str, text_position:str) -> None:
        self.__title_obj = _Title(font, font_size, text, text_position)
    
    def _compute_layout(self) -> [ImageDraw.Image, ImageDraw.ImageDraw]:
        draw_area = self.__draw_area_obj
        title = self.__title_obj
        self.__width = draw_area.get_width()
        self.__height = draw_area.get_height()
        if title is not None:
            title.set_width(self.__width)
            height_increment = title.get_height()
            self.__height += height_increment
            self.__title_ends = height_increment
        
        image = Image.new('RGB', (self.__width, self.__height), self.__background_color)
        draw = ImageDraw.Draw(image)
        
        return image, draw
    
    def get_image(self) -> ImageDraw.Image:
        image, draw_context = self._compute_layout()
        draw_area = self.__draw_area_obj
        title = self.__title_obj
        
        if title is not None:
            title.draw_lable(draw_context=draw_context)
            
        chains_storage = draw_area.get_chains_storage()
        previous_chain_end = self.__title_ends
        for chain in chains_storage:
            for shape in chain.get_shapes():
                shape.draw_shape(draw_context=draw_context, offset=previous_chain_end)
            previous_chain_end += chain.get_height()
            
        return image   
        
            

class _BaseCanvasComponent(ABC):
    def __init__(self):
        self._width = 0
        self._height = 0
        
    def get_height(self) -> int:
        return self._height

    def set_height(self, height: int) -> None:
        self._height = height

    def get_width(self) -> int:
        return self._width

    def set_width(self, width: int) -> None:
        self._width = width
    
class _Title(_BaseCanvasComponent):
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
        label.draw_label(draw_context)
    
    def _count_x0(self) -> None:
    	self.__text_x0 = int( self._width
    	                * self.__text_x_offset_multiplier
    	                - self.__font_size
    	                * 0.3 * len(self.__text))
    
    def _set_x_offset(self, text_position: str):
        text_x_offsets = {'centered': 0.5, 'right': 0.1, 'left': 0.9}
        return text_x_offsets.get(text_position, 0.1)
        
    
    
class _DrawArea(_BaseCanvasComponent):
    def __init__(self):
        super().__init__()
        self.__chains_storage = []
        
    def add_chain(self, chain: 'Chain') -> None:
        current_chain_width = chain.get_width()
        if current_chain_width > self._width:
            self._width = current_chain_width
        
        current_chain_height = chain.get_height()
        self._height += current_chain_height
        self.__chains_storage.append(chain)
    
    def get_chains_storage(self) -> list:
        return self.__chains_storage
