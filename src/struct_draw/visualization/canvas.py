from PIL import Image, ImageDraw, ImageFont
from .canvas_components import Title, DrawArea

class Canvas:
    def __init__(self, background_color: str):
        self.__background_color = background_color
        self.__title_obj = None
        self.__legend_obj = None
        self.__draw_area_obj = DrawArea()
        self.__height = 0
        self.__width = 0
        self.__title_ends = 0
        	
    def add_chain(self, chain: 'Chain', shape_size: int, annotate: bool = False, split:int = None) -> None:
        self.__draw_area_obj.add_chain(chain, shape_size,
                                       annotate=annotate,
                                       split=split)
        
    def add_title(self, font:str, font_size:int, text:str, text_position:str) -> None:
        self.__title_obj = Title(font, font_size, text, text_position)
    
    def _compute_layout(self) -> [ImageDraw.Image, ImageDraw.ImageDraw]:
        draw_area = self.__draw_area_obj
        title = self.__title_obj
        draw_area.compute_size()
        self.__width = draw_area.width
        self.__height = draw_area.height
        if title is not None:
            title.set_width(self.__width)
            height_increment = title.height
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
            
        previous_chain_end = self.__title_ends
        for chain in draw_area.chains:
            chain.draw_chain(draw_context, previous_chain_end)
            previous_chain_end += chain.height
            
        return image   
