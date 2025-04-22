from typing import Optional, Dict

import numpy as np

from .chain_base_area import BaseArea
from struct_draw.plotter.small_units.shape import Other, Helix, Strand, Gap
from .color_mods.mode_factory import create_mode

class ShapesArea(BaseArea):
    """
    Class for arranging and drawing shapes representing a sequence of residues.

    This class slices a Chain of residues into rows (splits) and manages the layout,
    coloring, and optional amino acid annotations for each residue shape.

    Attributes:
        _start (int): Starting index of residues to display.
        _end (int): End index (exclusive) of residues to display.
        __chain (Chain): Chain object containing residue list.
        __residues_quantity (int): Number of residues in the selected range.
        __shape_size (int): Pixel size for each shape.
        _split_info (Dict[str, int]): Info dict with keys 'full_chunk_size', 'last_chunk_size', 'split_levels'.
        _show_amino_code (bool): Flag to draw one-letter amino acid codes.
        _palette: Color palette instance for residues.
        __shapes_storage (np.ndarray): Array storing created shape instances.
    """
    def __init__( self, chain: 'Chain', shape_size: int, split: Optional[int] = None,
                  show_amino_code: bool = True, start: int = 0, end: Optional[int] = None,
                  color_mode: str = 'structure', color_sub_mode: str = 'secondary',
                  custom_palette: Optional[Dict[str, str]] = None):
        self._start = start
        self._end = end if end is not None else len(chain.residues)
        self.__chain = chain
        self.__residues_quantity = len(self.__chain.residues[self._start:self._end])
        self.__shape_size = shape_size
        self._split_info = self._compute_split_info(split)
        self._show_amino_code = show_amino_code
        self._palette = create_mode(color_mode, color_sub_mode, custom_palette)
        self.__shapes_storage = self._generate_shapes()
    
    
    @property 
    def width(self) -> int:
        margin = self.__shape_size * 2
        return self._split_info['full_chunk_size'] * self.__shape_size + margin
    
    @property
    def height(self) -> int:
        margin = self.__shape_size
        residue_height = self.__shapes_storage[0].height
        return residue_height * self._split_info['split_levels'] + margin 
        
    def _compute_split_info(self, split: Optional[int]) -> Dict[str, int]:
        """
        Computes how to split residues into rows.

        Args:
            split (Optional[int]): Max shapes per row, or None for no split.

        Returns:
            Dict[str, int]: Contains 'full_chunk_size', 'last_chunk_size', 'split_levels'.
        """
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
     
               
    def _generate_shapes(self) -> np.ndarray:
        """
        Creates and configures shape instances for each residue.

        Uses residue.secondary_structure to select shape class and tracks
        sub-structure positions for rendering transitions.

        Returns:
            np.ndarray: Array of shape objects.
        """
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
        structure_classes = {'Helix': Helix,
                             'Strand': Strand,
                             'Other': Other,
                             'gap': Gap}
                      
        
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

            fillcolor = self._palette.get_color(residue)
            shape_storage[i] = shape(residue, self.__shape_size,
                                     fillcolor, self._show_amino_code, sub_structure_shape_pos)

            if is_differen_sub_structure:
                sub_structure_shape_pos = 'first'
                is_differen_sub_structure = False
            else:
                sub_structure_shape_pos = 'inner'
            
        return shape_storage
        
        
        
    def draw(self, draw_context: 'ImageDraw.ImageDraw', y_offset: int, x_offset: int) -> None:
        """
        Draws all residue shapes arranged in rows with specified offsets.

        Args:
            draw_context (ImageDraw.ImageDraw): The PIL drawing context.
            y_offset (int): Vertical offset to start drawing.
            x_offset (int): Horizontal offset to start drawing.
        """
        full_chunk_size = self._split_info['full_chunk_size']
        last_chunk_size = self._split_info['last_chunk_size']
        split_levels = self._split_info['split_levels']
        y_0 = y_offset
        padding = self.__shape_size
        
        for level in range(split_levels - (1 if last_chunk_size else 0)):
            start = level * full_chunk_size
            end = start + full_chunk_size
            for i in range(start, end):
                x_0 = (i - start) * self.__shape_size + padding + x_offset
                self.__shapes_storage[i].draw(x_0, y_0, draw_context)
            y_0 += max(shape.height for shape in self.__shapes_storage[start:end])
         
        if last_chunk_size:
            start = (split_levels - 1) * full_chunk_size
            end = start + last_chunk_size
            for i in range(start, end):       
                x_0 = (i - start) * self.__shape_size + padding + x_offset
                self.__shapes_storage[i].draw(x_0, y_0, draw_context)
