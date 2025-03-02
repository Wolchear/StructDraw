from PIL import Image, ImageDraw, ImageFont

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
        self.__draw_area_obj._add_chain(chain)
        
    def add_title(self, font:str, font_size:int, text:str, text_position:str) -> None:
        self.__title_obj = _Title(font, font_size, text, text_position)
    
    def _compute_layout(self) -> None:
        draw_area = self.__draw_area_obj
        title = self.__title_obj
        self.__width = draw_area._get_width()
        self.__height = draw_area._get_height()
        if title is not None:
            title._set_width_x0(self.__width)
            height_increment = title._get_height()
            self.__height += height_increment
            self.__title_ends = height_increment
    
    def get_image(self):
        self._compute_layout()
        draw_area = self.__draw_area_obj
        title = self.__title_obj
        
        image_width = self.__width
        image_height = self.__height
        image = Image.new('RGB', (image_width, image_height), self.__background_color)
        draw = ImageDraw.Draw(image)
        if title is not None:
            font = title._get_font_object()
            text = title._get_text()
            cords = title._get_text_cords()
            draw.text(cords, text, font=font, fill=(0, 0, 0))
            
        chains_storage = draw_area._get_chains_storage()
        previous_chain_end = self.__title_ends
        for chain in chains_storage:
            for shape in chain.get_shapes():
                shape_tuple, info_tuple = shape.get_shape_params()
                cords = shape_tuple[0]
                cords[1] += previous_chain_end
                cords[3] += previous_chain_end
                color = shape_tuple[1]
                outline = shape_tuple[2]
                draw.rectangle(cords, fill=color, outline=outline)
            previous_chain_end += chain.get_heigth()
        return image   
        
            

class _Title:
    def __init__(self, font:str, font_size:int, text:str, text_position:str):
        self.__font_size = font_size
        self.__font = ImageFont.truetype(font, self.__font_size)
        self.__text = text
        self.__text_length = len(self.__text)
        self.__height = int(self.__font_size + self.__font_size * 0.5)
        self.__width = None
        self.__text_x_offsets = {'centered': 0.5, 'right': 0.1, 'left': 0.9}
        self.__text_x_offset_multiplier = self.__text_x_offsets.get(text_position, 0.25)
        self.__text_y0 = self.__height * 0.5 - 0.5 * self.__font_size
        self.__text_x0 = None
        
    def _set_width_x0(self, image_width: int) -> None:
    	self.__width = image_width
    	self.__text_x0 = ( image_width
    	                * self.__text_x_offset_multiplier
    	                - self.__font_size
    	                * 0.3 * self.__text_length )
    	
    def _get_height(self) -> int:
        return self.__height
        
    def _get_text_cords(self) -> tuple[int, int]:
        return (self.__text_x0, self.__text_y0)
    
    def _get_font_object(self) -> ImageFont.FreeTypeFont:
        return self.__font
    
    def _get_text(self) -> str:
        return self.__text
    
class _DrawArea:
    def __init__(self):
        self.__chains_storage = []
        self.__height = 0
        self.__width = 0
        
    def _add_chain(self, chain: 'Chain') -> None:
        current_chain_width = chain.get_width()
        if current_chain_width > self.__width:
            self.__width = current_chain_width
        
        current_chain_height = chain.get_heigth()
        self.__height += current_chain_height
        self.__chains_storage.append(chain)
    
    def _get_chains_storage(self) -> list:
        return self.__chains_storage
    
    def _get_width(self) -> int:
        return self.__width
    
    def _get_height(self) -> int:
    	return self.__height
