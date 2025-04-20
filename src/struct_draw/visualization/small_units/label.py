from dataclasses import dataclass, field
from PIL import ImageFont
from typing import Union, Tuple

@dataclass
class RegularLabel():
    _text: str
    _font_size: int
    _font: str
    _fill: Union[str, Tuple[int, int, int]] = field(default="#000000")
    
    def __post_init__(self):
        self._font_obj = ImageFont.truetype(self._font, self._font_size)
        bbox = self._font_obj.getbbox(self._text)
        self._offset_x, self._offset_y = bbox[0], bbox[1]
        self._text_width = bbox[2] - bbox[0]
        self._text_height = bbox[3] - bbox[1]
    
    @property
    def height(self) -> int:
        return self._text_height
        
    @property
    def width(self) -> int:
        return self._text_width
    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        draw_context.text([x_0, y_0],
                          text=self._text,
                          font=self._font_obj,
                          fill=self._fill)
