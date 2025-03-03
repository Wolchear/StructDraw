import numpy as np

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont

class Chain:
    def __init__(self, chain_data: np.ndarray, color_structures: str, shape_size: int, split: int = None):
        self.__chain_data = chain_data
        self.__residues_quantity = len(chain_data)
        self.__color_structures = color_structures
        self.__shape_size = shape_size
        self.__split = split
        padding = self.__shape_size * 2
        if self.__split is not None:
            self.__width = self.__split * self.__shape_size + padding
            self.__height = ( padding + ( self.__residues_quantity // self.__split )
                            * self.__shape_size )
        else:
            self.__width = self.__residues_quantity * self.__shape_size + padding
            self.__height = 2 * self.__shape_size
        self.__shapes_storage = self._generate_shapes()
    
    def _generate_shapes(self):
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
        structure_classes = {'H': Helix, 'I': Helix, 'G': Helix, 'P': Helix,
                            'B': Strand, 'E': Strand, 'T': Other, 'S': Other}
                      
        structure_colors = {'Helix': 'green',
                            'Strand': 'blue',
                            'Other': 'white'}
        
        
        split_level = 0
        x_split_offset = 0          
        for index, row in enumerate(self.__chain_data):
            if ( self.__split is not None and
                 index % self.__split == 0 and
                 index != 0 ):        
                    split_level += 1   
                    x_split_offset += self.__split    
                
            ss = row['SS']
            aa = row['AA']
            residue_index = row['residue_index']
            insertion_code = row['insertion_code']
            structure_class = structure_classes.get(ss, Other)
            fillcolor = structure_colors[structure_class.__name__]
            inner_padding = self.__shape_size * 0.5
            x0 = (index - x_split_offset) * self.__shape_size +  2 * inner_padding
            y0 = split_level * self.__shape_size + inner_padding
            shape_storage[index] = structure_class(self.__shape_size, residue_index,
                                         insertion_code, fillcolor, aa, ss, x0, y0)
         
        return shape_storage
                                                 
    def get_shapes(self):
        return self.__shapes_storage
        
    def get_width(self):
        return self.__width
        
    def get_height(self):
        return self.__height

@dataclass
class BaseShape(ABC):
    _size: int
    _residue_index: int
    _insertion_code: str
    _color: str
    _amino_acid: str
    _secondary_structure: str
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
class AnotationLable(BaseShape):
    def draw_shape(self, draw_context: ImageDraw.ImageDraw, offset: int) -> None:
        pass


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
