from dataclasses import dataclass, field
from typing import Dict, Optional
from abc import ABC, abstractmethod
from math import ceil

from PIL import Image, ImageDraw, ImageFont, ImageColor
from .label import RegularLabel

@dataclass
class BaseShape(ABC):
    _residue: object
    _size: int
    _color: str
    _show_amino_code: bool
    _pos_in_structure: str
    _amino_label: object = field(init=False)
    _font_size: int = field(init=False)
    _font: str = field(default='DejaVuSans.ttf')
    _font_color: str = field(init=False)

    @property
    def height(self):   
        return self._size
    
    def __post_init__(self) -> None:
        if self._show_amino_code:
            self._font_color = self.get_contrast_color(self._color)
            self._font_size =  self._size * 0.4
            self._amino_label = self._generate_amino_annotation()
    
    
    def get_contrast_color(self, bg_color: str, threshold: int = 128) -> str:
        """
        Retuns '#FFFF99' if bg_color is dark
        Returns '#000000' if bg_color is light.
        bg_color:
          - #RRGGBB' or
          - Color name (ex.: white, red, blue,...)
        """
        r, g, b = ImageColor.getrgb(bg_color)
        luminance = 0.299*r + 0.587*g + 0.114*b
        return '#FFFF99' if luminance < threshold else '#000000' 
     
    
    def _generate_amino_annotation(self) -> RegularLabel:
        return RegularLabel(self._residue.amino_acid, self._font_size, self._font, self._font_color)
    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        self._draw_self(x_0, y_0, draw_context)
        amino_label_x_0 = x_0 + int(self._size * 0.5)
        if self._show_amino_code:
            amino_label_x_0 = x_0 + (self._size - self._amino_label.width) // 2
            amino_label_y_0 = y_0 + (self._size - self._amino_label.height) // 2
            
            adjusted_x = amino_label_x_0 - self._amino_label._offset_x
            adjusted_y = amino_label_y_0 - self._amino_label._offset_y
            
            self._amino_label.draw(adjusted_x, adjusted_y, draw_context)
    
        
    @abstractmethod
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        pass

            
@dataclass        
class Other(BaseShape):    
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        fixed_y_0 = y_0 + int(self._size * 0.3)
        fixed_y_1 = y_0 + int(self._size * 0.7)
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.03)
        draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        
     
@dataclass
class Helix(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        points = []
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.05)
        if self._pos_in_structure == 'first':
            points = [ (x_0,                         y_0 + int(self._size * 0.3)), # A
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.3)), # B
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.1)), # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.1)), # D
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # E
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.5)), # F
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.7)), # G
                       (x_0,                         y_0 + int(self._size * 0.7))] # H
        elif self._pos_in_structure == 'inner':
            points = [ (x_0,                         y_0 + int(self._size * 0.1)), # A
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.1)), # B
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.25)),# C
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.25)),# D
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.1)), # E
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.1)), # F
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # G
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.5)), # H
                       (x_0 + int(self._size * 0.7), y_0 + int(self._size * 0.7)), # K
                       (x_0 + int(self._size * 0.3), y_0 + int(self._size * 0.7)), # L
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.5)), # M
                       (x_0,                         y_0 + int(self._size * 0.5))] # N
        elif self._pos_in_structure == 'last':
            points = [ (x_0,                         y_0 + int(self._size * 0.1)), # A
                       (x_0 + int(self._size * 0.5), y_0 + int(self._size * 0.1)), # B
                       (x_0 + int(self._size * 0.7), y_0 + int(self._size * 0.3)), # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.3)), # D
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.7)), # E
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.7)), # F
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.5)), # G
                       (x_0,                         y_0 + int(self._size * 0.5))] # H
                       
                  
        draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)

@dataclass
class Strand(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        outline_width = ceil(self._size * 0.05)
        if self._pos_in_structure == 'first' or self._pos_in_structure == 'inner':
            x_1 = x_0 + self._size
            fixed_y_0 = y_0 + int(self._size * 0.2)
            fixed_y_1 = y_0 + int(self._size * 0.8)
            draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        else:
            points = [ (x_0,                         y_0 + int(self._size * 0.2)), # A
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.2)), # B
                       (x_0 + int(self._size * 0.4), y_0),                         # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # D
                       (x_0 + int(self._size * 0.4), y_0 + self._size),            # E
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.8)), # F
                       (x_0,                         y_0 + int(self._size * 0.8))] # G
            draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)
        
        
@dataclass
class Gap(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        y_0 = y_0 + 0.5 * self._size
        margin = self._size * 0.1
        width = ceil(self._size * 0.05)
        draw_context.line([x_0 + margin, y_0, x_1 - margin, y_0],
                                   		fill='black')
