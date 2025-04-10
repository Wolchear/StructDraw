from dataclasses import dataclass, field
from typing import Dict, Optional
from abc import ABC, abstractmethod
from math import ceil

from PIL import Image, ImageDraw, ImageFont
from .label import RegularLabel

@dataclass
class BaseShape(ABC):
    _residue: object
    _size: int
    _color: str
    _show_amino_code: bool
    _pos_in_structure: str
    _amino_label: object = field(init=False)
    _annotate: Optional[Dict[str, bool]] = field(default=None)
    _annotation_labels: Optional[list] = field(init=False)
    _font_size: int = field(init=False)
    _font: str = field(default='DejaVuSans.ttf')

    @property
    def height(self):
        height = self._size
        if self._annotate is not None:
            for label in self._annotation_labels:
                height += label.height     
        return height
    
    def __post_init__(self) -> None:
        self._font_size =  self._size * 0.4
        self._annotation_labels = []
        if self._show_amino_code:
        	self._amino_label = self._generate_amino_annotation()
        if self._annotate is not None:
           self._generate_annotation_labels()
    
    
    def _generate_amino_annotation(self) -> RegularLabel:
        return RegularLabel(self._residue.amino_acid, self._font_size, self._font)
    
    def _generate_annotation_labels(self) -> None:
        to_annotate_list = list(self._annotate.keys())
        offset = self._size
        for key in to_annotate_list:
            self._annotation_labels.append(RegularLabel(getattr(self._residue, key),
                                                        self._font_size, self._font))
    
    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        self._draw_self(x_0, y_0, draw_context)
        amino_label_x_0 = x_0 + int(self._size * 0.5)
        if self._show_amino_code:
            amino_label_x_0 = x_0 + (self._size - self._amino_label.width) // 2
            amino_label_y_0 = y_0 + (self._size - self._amino_label.height) // 2
            
            adjusted_x = amino_label_x_0 - self._amino_label._offset_x
            adjusted_y = amino_label_y_0 - self._amino_label._offset_y
            
            self._amino_label.draw(adjusted_x, adjusted_y, draw_context)
        y_1 = y_0 + self._size
        self._draw_annotation_labels(x_0, y_1, draw_context)
    
        
    @abstractmethod
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        pass
    
    
    def _draw_annotation_labels(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        for label in self._annotation_labels:
            label.draw(x_0, y_0, draw_context)
            y_0 += label.height
            
@dataclass        
class Other(BaseShape):    
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        fixed_y_0 = y_0 + int(self._size * 0.3)
        fixed_y_1 = y_0 + int(self._size * 0.7)
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.05)
        draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        
     
@dataclass
class Helix(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.05)
        points = [(x_0, y_0 + int(self._size * 0.4)),                         #A
                  (x_0 + int(self._size * 0.1), y_0 +int(self._size * 0.4)),  #B
                  (x_0 + int(self._size * 0.05), y_0),                        #C
                  (x_0 + int(self._size * 0.4), y_0),                         #D
                  (x_0 + int(self._size * 0.5), y_0 + int(self._size * 0.4)), #E
                  (x_0 + int(self._size * 0.6), y_0),                         #F
                  (x_0 + int(self._size * 0.8), y_0),                         #G
                  (x_0 + int(self._size * 0.9), y_0 + int(self._size * 0.4)), #H
                  (x_0 + int(self._size), y_0 + int(self._size * 0.4)),       #I
                  (x_0 + int(self._size), y_0 + int(self._size * 0.6)),       #J
                  (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.6)), #K
                  (x_0 + int(self._size * 0.75), y_0 + int(self._size * 0.6)),#L
                  (x_0 + int(self._size * 0.6), y_1),                         #M
                  (x_0 + int(self._size * 0.4), y_1),                         #N
                  (x_0 + int(self._size * 0.25), y_0 + int(self._size * 0.6)),#O
                  (x_0, y_0 + int(self._size * 0.6))]                         #R
                  
        draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)

@dataclass
class Strand(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        outline_width = ceil(self._size * 0.05)
        x_1 = x_0 + self._size
        if self._pos_in_structure == 'first' or self._pos_in_structure == 'inner':
            fixed_y_0 = y_0 + int(self._size * 0.2)
            fixed_y_1 = y_0 + int(self._size * 0.8)
            draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        else:
            points = [ (x_0, y_0 + int(self._size * 0.2)),                         # A
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.2)), # B
                       (x_0 + int(self._size * 0.4), y_0),                         # C
                       (x_1, y_0 + int(self._size * 0.5)),                         # D
                       (x_0 + int(self._size * 0.4), y_0 + self._size),            # E
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.8)), # F
                       (x_0, y_0 + int(self._size * 0.8))]                         # G
            draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)
        
        
@dataclass
class Gap(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        y_0 = y_0 + 0.5 * self._size
        margin = self._size * 0.1
        draw_context.line([x_0 + margin, y_0, x_1 - margin, y_0],
                                   		fill=self._color)
