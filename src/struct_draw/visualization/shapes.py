import numpy as np

from typing import Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont


class Chain:
    def __init__(self, chain: 'Chain', color_structures: str, shape_size: int, split: int = None):
        self.__chain = chain
        self.__residues_quantity = len(self.__chain.residues)
        self.__color_structures = color_structures
        self.__shape_size = shape_size
        self.__split = split
        margin = self.__shape_size * 2
        self.__chain_label = self._generate_label()
        if self.__split is not None:
            self.__width = self.__split * self.__shape_size + margin
            self.__height = ( margin + ( self.__residues_quantity // self.__split )
                            * self.__shape_size )
        else:
            self.__width = self.__residues_quantity * self.__shape_size + margin
            self.__height = 2 * self.__shape_size
        self.__shapes_storage = self._generate_shapes()
    
    
    def _generate_label(self):
        chain_id = self.__chain.chain_id
        x_0 = self.__shape_size * 0.1
        y_0 = self.__shape_size
        return RegularLabel(x_0, y_0, chain_id, self.__shape_size, 'DejaVuSans.ttf')
    
    def _generate_shapes(self):
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
        structure_classes = {'H': Helix, 'I': Helix, 'G': Helix, 'P': Helix,
                            'B': Strand, 'E': Strand, 'T': Other, 'S': Other}
                      
        structure_colors = {'Helix': 'green',
                            'Strand': 'blue',
                            'Other': 'white'}
        
        
        split_level = 0
        x_split_offset = 0          
        for index, row in enumerate(self.__chain.residues):
            if ( self.__split is not None and
                 index % self.__split == 0 and
                 index != 0 ):        
                    split_level += 1   
                    x_split_offset += self.__split    
                
            ss = self.__chain.secondary_structure[index]
            structure_class = structure_classes.get(ss, Other)
            fillcolor = structure_colors[structure_class.__name__]
            padding = self.__shape_size
            x0 = (index - x_split_offset) * self.__shape_size +  padding
            y0 = split_level * self.__shape_size + padding
            shape_storage[index] = structure_class(self.__shape_size, fillcolor, x0, y0)
         
        return shape_storage
                                                 
    def get_shapes(self):
        return self.__shapes_storage
        
    def get_width(self):
        return self.__width
        
    def get_height(self):
        return self.__height
        
    
    def draw_chain(self, draw_context, offset: int) -> None:
        self.__chain_label.draw_label(draw_context=draw_context, offset=offset)
        for shape in self.get_shapes():
                shape.draw_shape(draw_context=draw_context, offset=offset)

@dataclass
class BaseShape(ABC):
    _size: int
    _color: str
    _x_0: int
    _y_0: int
    _x_1: int = field(init=False)
    _y_1: int = field(init=False)

    def __post_init__(self):
        self._x_1 = self._x_0 + self._size
        self._y_1 = self._y_0 + self._size
    
    @abstractmethod
    def draw_shape(self):
        pass

@dataclass        
class Other(BaseShape):    
    def draw_shape(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        draw_context.rectangle([self._x_0, self._y_0 + offset,
                                self._x_1, self._y_1 + offset],
                                fill=self._color, outline='black')
     
@dataclass
class Helix(BaseShape):
    def draw_shape(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        draw_context.line([self._x_0, self._y_0 + offset,
                              self._x_1, self._y_1 + offset],
                              fill=self._color)

@dataclass
class Strand(BaseShape):
    def draw_shape(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        draw_context.ellipse([self._x_0, self._y_0 + offset,
                              self._x_1, self._y_1 + offset],
                              fill=self._color, outline='black')
                              
        
@dataclass
class RegularLabel():
    _x_0: int
    _y_0: int
    _text: str
    _font_size: int
    _font: str
    
    def __post_init__(self):
        self._font_obj = ImageFont.truetype(self._font, self._font_size)
    
    def draw_label(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        draw_context.text([self._x_0, self._y_0 + offset], self._text, font=self._font_obj, fill=(0, 0, 0))          

                  
@dataclass
class AnotationLabel(RegularLabel):
    __residue_index: int 
    __insertion_code: str
    __amino_acid: str
    __secondary_structure: str
    
    def draw_label(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        draw_context.text([self._x_0, self._y_0  + offset], self._text, font=self._font_obj, fill=(0, 0, 0))                             
