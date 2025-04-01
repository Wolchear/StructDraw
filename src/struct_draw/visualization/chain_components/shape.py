from dataclasses import dataclass, field
from typing import Dict, Optional
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw, ImageFont
from .label import RegularLabel

@dataclass
class BaseShape(ABC):
    _residue: object
    _size: int
    _color: str
    _annotate: Optional[Dict[str, bool]] = field(default=None)
    _annotation_labels: Optional[list] = field(init=False)
    _font_size: int = field(default=12)
    _font: str = field(default='DejaVuSans.ttf')

    @property
    def height(self):
        height = self._size
        if self._annotate is not None:
            for label in self._annotation_labels:
                height += label.height     
        return height
    
    def __post_init__(self) -> None:
        self._annotation_labels = []
        if self._annotate is not None:
           self._generate_annotation_labels()
    
    
    def _generate_annotation_labels(self) -> None:
        to_annotate_list = list(self._annotate.keys())
        offset = self._size
        for key in to_annotate_list:
            self._annotation_labels.append(RegularLabel(getattr(self._residue, key),
                                                        self._font_size, self._font))
    
    @abstractmethod
    def draw(self) -> None:
        pass
        
    
    def draw_annotation_labels(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        for label in self._annotation_labels:
            label.draw(x_0, y_0, draw_context, offset)
            offset += label.height
            
@dataclass        
class Other(BaseShape):    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        #print('Other:', x_0, y_0)
        draw_context.rectangle([x_0, y_0 + offset, x_1, y_1 + offset],
                                    fill=self._color, outline='black')
        self.draw_annotation_labels(x_0, y_1, draw_context, offset)
     
@dataclass
class Helix(BaseShape):
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        fixed_y_0 = y_0 + offset
        x_1 = x_0 + self._size
        y_1 = fixed_y_0 + self._size
        
        points = [(x_0, fixed_y_0 + int(self._size * 0.4)),                         #A
                  (x_0 + int(self._size * 0.1), fixed_y_0 +int(self._size * 0.4)),  #B
                  (x_0 + int(self._size * 0.05), fixed_y_0),                         #C
                  (x_0 + int(self._size * 0.4), fixed_y_0),                         #D
                  (x_0 + int(self._size * 0.5), fixed_y_0 + int(self._size * 0.4)), #E
                  (x_0 + int(self._size * 0.6), fixed_y_0),                         #F
                  (x_0 + int(self._size * 0.8), fixed_y_0),                         #G
                  (x_0 + int(self._size * 0.9), fixed_y_0 + int(self._size * 0.4)), #H
                  (x_0 + int(self._size), fixed_y_0 + int(self._size * 0.4)),       #I
                  (x_0 + int(self._size), fixed_y_0 + int(self._size * 0.6)),       #J
                  (x_0 + int(self._size * 0.8), fixed_y_0 + int(self._size * 0.6)), #K
                  (x_0 + int(self._size * 0.75), fixed_y_0 + int(self._size * 0.6)), #L
                  (x_0 + int(self._size * 0.6), y_1),                               #M
                  (x_0 + int(self._size * 0.4), y_1),                               #N
                  (x_0 + int(self._size * 0.25), fixed_y_0 + int(self._size * 0.6)), #O
                  (x_0, fixed_y_0 + int(self._size * 0.6))]                         #R
                  
        draw_context.polygon(points, outline="black", fill=self._color)
        self.draw_annotation_labels(x_0, y_0 + self._size, draw_context, offset)

@dataclass
class Strand(BaseShape):
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        #print('Strand:', x_0, y_0)
        draw_context.ellipse([x_0, y_0 + offset, x_1, y_1 + offset],
                                   fill=self._color, outline='black')
        self.draw_annotation_labels(x_0, y_1, draw_context, offset)
        
        
@dataclass
class Gap(BaseShape):
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        y_0 = y_0 + 0.5 * self._size
        margin = self._size * 0.1
        draw_context.line([x_0 + margin, y_0 + offset, x_1 - margin, y_0 + offset],
                                   		fill=self._color)
        self.draw_annotation_labels(x_0, y_1, draw_context, offset)
