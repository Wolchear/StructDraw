from typing import Optional, Dict

import numpy as np

from struct_draw.plotter.chain_components import ShapesArea, AnnotationArea

CHAIN_DEFAULT_ANNOTATION = {'chain_id': True,
                            'algorithm': False,
                            'model_id': True}

class Chain:
    """
    Orchestrates the visualization of a molecular chain by combining an annotation area and a shapes area.

    Attributes:
        __chain (Chain): Underlying chain data structure.
        __shape_size (int): Base size for rendering shapes and text.
        _annotation_area (AnnotationArea): Area for rendering textual annotations.
        _shapes_area (ShapesArea): Area for rendering graphical shapes of the chain.
    Args:
        chain (Chain): The chain data to visualize.
        shape_size (int): Base size for shapes and text.
        show_amino_code (bool): Whether to display amino acid codes on shapes.
        split (Optional[int]): Position at which to split the chain visualization.
        start (int): Index of the first residue to render.
        end (Optional[int]): Index of the last residue to render.
        chain_annotation (Dict[str, bool]): Flags for which chain attributes to annotate.
        color_mode (str): Primary coloring mode (e.g., 'structure', 'hydrophobicity').
        color_sub_mode (str): Secondary coloring granularity (e.g., 'secondary', 'single_aa').
        custom_palette (Optional[Dict[str, str]]): Mapping of categories to custom colors.
    """
    def __init__(self, chain: 'Chain', shape_size: int, show_amino_code: bool = True, split: Optional[int] = None,
                 start: int = 0, end: Optional[int] = None, chain_annotation: Dict[str, bool] = CHAIN_DEFAULT_ANNOTATION,
                 color_mode: str = 'structure', color_sub_mode: str = 'secondary', custom_palette: Optional[Dict[str, str]] = None):
        self.__chain = chain
        self.__shape_size = shape_size
        self._annotation_area = AnnotationArea( chain=chain,
                                                chain_annotation=chain_annotation,
                                                font_size=shape_size )
        self._shapes_area = ShapesArea( chain=chain, shape_size=shape_size,
                                        show_amino_code=show_amino_code,
                                        split=split, start=start, end=end,
                                        color_mode=color_mode, color_sub_mode=color_sub_mode,
                                        custom_palette=custom_palette)
        
    @property 
    def width(self) -> int:
        return self._shapes_area.width + self._annotation_area.width
    
    @property
    def height(self) -> int:
        return max(self._shapes_area.height, self._annotation_area.height)
    
    @property
    def annotation_area(self) -> list:
        return self._annotation_area
    
    def draw(self, draw_context: 'ImageDraw.ImageDraw', y_offset: int, x_offset: int) -> None:
        """
        Draw both annotation and shape areas onto the provided drawing context.

        Args:
            draw_context (ImageDraw.ImageDraw): PIL drawing context.
            y_offset (int): Vertical offset at which to start drawing.
            x_offset (int): Horizontal offset at which shapes area begins.
        """
        self._annotation_area.draw(draw_context=draw_context, y_offset=y_offset)
        self._shapes_area.draw(draw_context=draw_context, y_offset=y_offset, x_offset=x_offset)
