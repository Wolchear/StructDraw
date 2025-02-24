from PIL import Image, ImageDraw, ImageFont

class Canvas:
    def __init__(self, background_color: str, font: str, font_size: int):
        self.__background_color = background_color
        self.__title_obj = None
        self.__legend_obj = None
        self.__draw_area_obj = _DrawArea(font, font_size)
        	
    def add_chain(self, chain):
        self.__draw_area_obj._add_chain(chain)
        
    def add_title(self, font, font_color, text, text_position):
        self.__title_obj = _Title(font, font_color, text, text_position)
    
    def get_image(self):
        draw_area = self.__draw_area_obj
        image_width = draw_area._get_width()
        image_height = draw_area._get_height()
        print(image_width)
        print(image_height)
        image = Image.new('RGB', (image_width, image_height), self.__background_color)
        
        chains_storage = draw_area._get_chains_storage()
        draw = ImageDraw.Draw(image)
        previous_chain_end = 0
        for chain in chains_storage:
            for shape in chain.get_shapes():
                shape_tuple, font_tuple, info_tuple = shape.get_shape_params()
                cords = shape_tuple[0]
                cords[1] += previous_chain_end
                cords[3] += previous_chain_end
                print(cords)
                color = shape_tuple[1]
                outline = shape_tuple[2]
                draw.rectangle(cords, fill=color, outline=outline)
            previous_chain_end += chain.get_heigth()
        return image   
        
            

class _Title:
    def __init__(self, font:str, font_size:int, text:str, text_position:str):
        self.__font = font
        self.__font_size = font_size
        self.__text = text
        self.__text_position = text_position
        self.__height = self.__font_size + self.__font_size * 0.5
        
class _DrawArea:
    def __init__(self, font, font_size: int):
        self.__font = font
        self.__font_size = font_size
        self.__chains_storage = []
        self.__height = 0
        self.__width = 0
        
    def _add_chain(self, chain):
        current_chain_width = chain.get_width()
        if current_chain_width > self.__width:
            self.__width = current_chain_width
        
        current_chain_height = chain.get_heigth()
        self.__height += current_chain_height
        self.__chains_storage.append(chain)
    
    def _get_chains_storage(self):
        return self.__chains_storage
    
    def _get_width(self):
        return self.__width
    
    def _get_height(self):
    	return self.__height
