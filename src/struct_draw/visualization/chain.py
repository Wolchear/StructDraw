from typing import Optional, Dict

import numpy as np

from struct_draw.visualization.chain_components import ShapesArea, AnnotationArea

CHAIN_DEFAULT_ANNOTATION = {'chain_id': True,
                            'algorithm': False,
                            'model_id': True}

class Chain:
    def __init__(self, chain: 'Chain', color_structures: str, shape_size: int,
                 show_amino_code: bool = True, split: Optional[int] = None,
                 start: int = 0, end: Optional[int] = None, chain_annotation: Dict[str, bool] = CHAIN_DEFAULT_ANNOTATION):
        self.__chain = chain
        self.__shape_size = shape_size
        self._annotation_area = AnnotationArea( chain=chain,
                                                chain_annotation=chain_annotation,
                                                font_size=shape_size )
        self._shapes_area = ShapesArea( chain=chain, shape_size=shape_size,
                                        show_amino_code=show_amino_code,
                                        split=split, start=start, end=end )
        
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
        self._annotation_area.draw(draw_context=draw_context, y_offset=y_offset)
        self._shapes_area.draw(draw_context=draw_context, y_offset=y_offset, x_offset=x_offset)
