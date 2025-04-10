from PIL import Image, ImageDraw, ImageFont
from .canvas_components import Title, DrawArea

class Canvas:
    def __init__(self, background_color: str):
        self.__background_color = background_color
        self._title = Title()
        self.__legend_obj = None
        self._draw_area = DrawArea()
        	
    def add_chain(self, chain: 'Chain', shape_size: int, show_amino_code: bool = True,
                  annotate: bool = None, split:int = None) -> None:
        self._draw_area.add_chain(chain, shape_size, show_amino_code,
                                  annotate, split)
        
    def add_title(self, font:str, font_size:int, text:str, text_position:str) -> None:
        self._title.add_label(font, font_size, text, text_position)
    
    def _compute_layout(self) -> [ImageDraw.Image, ImageDraw.ImageDraw]:        
        self._draw_area.compute_size()
        self._title.compute_size(self._draw_area.width)
        
        image_width = self._draw_area.width
        image_height = self._draw_area.height + self._title.height
        
        image = Image.new('RGB', (image_width, image_height), self.__background_color)
        draw = ImageDraw.Draw(image)
        
        return image, draw
    
    def get_image(self) -> ImageDraw.Image:
        image, draw_context = self._compute_layout()
        self._title.draw(draw_context=draw_context)
            
        self._draw_area.draw(draw_context, self._title.height)
            
        return image   
