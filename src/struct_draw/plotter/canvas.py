from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from .canvas_components import Title, DrawArea
from struct_draw.plotter.canvas_components import Title, DrawArea

class Canvas:
    """
    Represents a drawing canvas that orchestrates the rendering of titles, chain visualizations, and layout.

    Attributes:
        __background_color (str): Background color for the canvas image.
        _title (Title): Title object managing text labels at the top.
        __legend_obj: Optional legend container, set via future methods.
        _draw_area (DrawArea): Area managing chain(s) placement and rendering.
    """
    def __init__(self, background_color: str):
        """
        Initialize a new Canvas with a specified background color.

        Args:
            background_color (str): RGB or hex string for canvas background.
        """
        self.__background_color = background_color
        self._title = Title()
        self.__legend_obj = None
        self._draw_area = DrawArea()
        	
    def add_chain(self, chain: 'Chain') -> None:
        """
        Add a Chain visualization to the drawing area.

        Args:
            chain (Chain): Chain instance to render on the canvas.
        """
        self._draw_area.add_chain(chain)
        
    def add_title(self, font:str, font_size:int, text:str, text_position:str) -> None:
        """
        Configure and add a title label to the canvas.

        Args:
            font (str): Font file or font name to use.
            font_size (int): Font size for title text.
            text (str): The title text to display.
            text_position (str): Position specifier (e.g., 'centered', 'left').
        """
        self._title.add_label(font, font_size, text, text_position)
    
    def _compute_layout(self) -> [ImageDraw.Image, ImageDraw.ImageDraw]:
        """
        Compute sizes of title and drawing areas, create a new image and draw context.

        Returns:
            Tuple[Image, ImageDraw.ImageDraw]: The PIL Image and drawing context.
        """        
        self._draw_area.compute_size()
        self._title.compute_size(self._draw_area.width)
        
        image_width = self._draw_area.width
        image_height = self._draw_area.height + self._title.height
        
        image = Image.new('RGB', (image_width, image_height), self.__background_color)
        draw = ImageDraw.Draw(image)
        
        return image, draw
    
    def get_image(self) -> ImageDraw.Image:
        """
        Render the full canvas including title and all chains, and return the final image.

        Returns:
            Image: A PIL Image containing the complete visualization.
        """
        image, draw_context = self._compute_layout()
        self._title.draw(draw_context=draw_context)
            
        self._draw_area.draw(draw_context, self._title.height)
            
        return image   
