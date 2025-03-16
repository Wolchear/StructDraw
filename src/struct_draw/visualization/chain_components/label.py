from dataclasses import dataclass, field
from PIL import ImageFont

@dataclass
class RegularLabel():
    _text: str
    _font_size: int
    _font: str
    
    def __post_init__(self):
        self._font_obj = ImageFont.truetype(self._font, self._font_size)
    
    @property
    def height(self) -> int:
        return self._font_size
        
    @property
    def width(self) -> int:
        return self._font_size * len(self._text)
    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        #print('Label_cords:', x_0, y_0 + offset)
        draw_context.text([x_0, y_0 + offset],
                          text=self._text, font=self._font_obj,
                          fill=(0, 0, 0))
