from typing import Optional, Dict

import numpy as np

from .chain_components.shape import Other, Helix, Strand, Gap
from .chain_components.label import RegularLabel

class Chain:
    def __init__(self, chain: 'Chain', color_structures: str, shape_size: int,
                 show_amino_code: bool = True, split: Optional[int] = None,
                 start: Optional[int] = None, end: Optional[int] = None):
        self._start = start - 1 if start is not None else 0
        self._end = end if end is not None else len(chain.residues)
        self.__chain = chain
        self.__residues_quantity = len(self.__chain.residues[self._start:self._end])
        self.__color_structures = color_structures
        self._show_amino_code = show_amino_code
        self.__shape_size = shape_size
        self._split_info = self._compute_split_info(split)
        self.__chain_label = self._generate_label()    
        self.__shapes_storage = self._generate_shapes()
        
    
    def _compute_split_info(self, split: Optional[int]) -> Dict[str, int]:
        if split is None:
            return {'full_chunk_size': self.__residues_quantity,
                    'last_chunk_size': 0,
                    'split_levels': 1}
        
        split_levels = ( self.__residues_quantity + split - 1) // split
        full_chunk_size = split
        last_chunk_size = ( self.__residues_quantity
                            - full_chunk_size
                            * (split_levels - 1 ))
                         
        return {'full_chunk_size': full_chunk_size,
                'last_chunk_size': last_chunk_size,
                'split_levels': split_levels}
    
    @property 
    def width(self) -> int:
        margin = self.__shape_size * 2
        return self._split_info['full_chunk_size'] * self.__shape_size + margin
    
    @property
    def height(self) -> int:
        margin = self.__shape_size
        residue_height = self.__shapes_storage[0].height
        return residue_height * self._split_info['split_levels'] + margin
    
    def _generate_label(self) -> RegularLabel:
        chain_id = self.__chain.chain_id
        return RegularLabel(chain_id, self.__shape_size, 'DejaVuSans.ttf')
    
    def _generate_shapes(self) -> np.ndarray:
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
        structure_classes = {'H': Helix, 'I': Helix, 'G': Helix, 'P': Helix,
                             'B': Strand, 'E': Strand, 'T': Other, 'S': Other,
                             'gap': Gap}
                      
        structure_colors = {'Helix': 'green',
                            'Strand': 'blue',
                            'Other': 'white',
                            'Gap': 'black'}
        
        sub_structure_shape_pos = 'first'
        is_differen_sub_structure = False
             
        for i, global_index in enumerate(range(self._start, self._end)):
            residue = self.__chain.residues[global_index]
            ss = residue.secondary_structure
            shape = structure_classes.get(ss, Other)
            
            if global_index != self._end - 1:
                next_shape = structure_classes.get(self.__chain.residues[global_index + 1].secondary_structure, Other)
                if shape != next_shape:
                    is_differen_sub_structure = True
                    sub_structure_shape_pos = 'last'
            else:
                sub_structure_shape_pos = 'last'

            fillcolor = structure_colors[shape.__name__]
            shape_storage[i] = shape(residue, self.__shape_size,
                                     fillcolor, self._show_amino_code, sub_structure_shape_pos)

            if is_differen_sub_structure:
                sub_structure_shape_pos = 'first'
                is_differen_sub_structure = False
            else:
                sub_structure_shape_pos = 'inner'
            
        return shape_storage
     
    def _draw_shapes(self, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        full_chunk_size = self._split_info['full_chunk_size']
        last_chunk_size = self._split_info['last_chunk_size']
        split_levels = self._split_info['split_levels']
        y_0 = offset
        padding = self.__shape_size
        
        for level in range(split_levels - (1 if last_chunk_size else 0)):
            start = level * full_chunk_size
            end = start + full_chunk_size
            for i in range(start, end):
                x_0 = (i - start) * self.__shape_size + padding
                self.__shapes_storage[i].draw(x_0, y_0, draw_context)
            y_0 += max(shape.height for shape in self.__shapes_storage[start:end])
         
        if last_chunk_size:
            start = (split_levels - 1) * full_chunk_size
            end = start + last_chunk_size
            for i in range(start, end):       
                x_0 = (i - start) * self.__shape_size + padding
                self.__shapes_storage[i].draw(x_0, y_0, draw_context)
    
    def draw(self, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        self.__chain_label.draw(0, offset, draw_context=draw_context)
        self._draw_shapes(draw_context=draw_context, offset=offset)        
