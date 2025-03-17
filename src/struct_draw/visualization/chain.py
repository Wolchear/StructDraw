import numpy as np

from typing import Optional, Dict
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from .chain_components.shape import Other, Helix, Strand, Gap
from .chain_components.label import RegularLabel


class Chain:
    def __init__(self, chain: 'Chain', color_structures: str,
                 shape_size: int, annotate: Dict[str, bool] = None, split: int = None):
        self.__chain = chain
        self.__residues_quantity = len(self.__chain.residues)
        self.__color_structures = color_structures
        self.__shape_size = shape_size
        self.__annotate = annotate
        self.__split = split
        self.__chain_label = self._generate_label()    
        self.__shapes_storage = self._generate_shapes()
    
        
    @property 
    def width(self) -> int:
        margin = self.__shape_size * 2
        if self.__split is not None:
            width = (self.__split
                     * self.__shape_size
                     + margin)
        else:
            width = (self.__residues_quantity
                    * self.__shape_size
                    + margin)
        return width
    
    @property
    def height(self) -> int:
        margin = self.__shape_size
        residue_height = self.__shapes_storage[0].height
        print(residue_height)
        if self.__split is not None:
            split_level = (self.__residues_quantity + self.__split - 1) // self.__split
            height = residue_height * split_level + margin
        else:
            height = residue_height + margin
        return height
    
    def _generate_label(self):
        chain_id = self.__chain.chain_id
        return RegularLabel(chain_id, self.__shape_size, 'DejaVuSans.ttf')
    
    def _generate_shapes(self):
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
        
        structure_classes = {'H': Helix, 'I': Helix, 'G': Helix, 'P': Helix,
                             'B': Strand, 'E': Strand, 'T': Other, 'S': Other,
                             'gap': Gap}
                      
        structure_colors = {'Helix': 'green',
                            'Strand': 'blue',
                            'Other': 'white',
                            'Gap': 'black'}
                    
        for index, residue in enumerate(self.__chain.residues):      
            ss = residue.secondary_structure
            shape = structure_classes.get(ss, Other)
            fillcolor = structure_colors[shape.__name__]
            shape_storage[index] = shape(residue, self.__shape_size,
                                   fillcolor, self.__annotate)
            
        return shape_storage
     
    def _draw_shapes(self,x_0, y_0, draw_context, offset: int):
        split_level = 0
        x_split_offset = 0        
        last_shape_y_offset = 0  
        for index, shape in enumerate(self.get_shapes()):
            if (self.__split is not None and
                index % self.__split == 0 and
                                  index != 0):        
                    split_level += 1   
                    x_split_offset += self.__split
                    last_shape_y_offset += shape.height
                    
            padding = self.__shape_size
            x_0 = (index - x_split_offset) * self.__shape_size + padding
            y_0 = last_shape_y_offset
            shape.draw(x_0, y_0, draw_context, offset)
                     
    def get_shapes(self):
        return self.__shapes_storage
    
    def draw_chain(self, draw_context, offset: int) -> None:
        self.__chain_label.draw(0, 0, draw_context=draw_context, offset=offset)
        self._draw_shapes(0, 0, draw_context=draw_context, offset=offset)        
