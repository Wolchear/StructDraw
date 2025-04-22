from typing import Optional, Dict

from .chain_base_area import BaseArea
from struct_draw.plotter.small_units.label import RegularLabel


class AnnotationArea(BaseArea):
    """
    AnnotationArea handles the layout and rendering size calculation for chain annotation labels.

    Attributes:
        _chain (Chain): The chain object containing attributes to annotate.
        _chain_annotation (Dict[str, bool]): A mapping of attribute names to booleans indicating whether to include the annotation.
        _font_size (int): Font size used for label rendering.
        _labels_storage (List[RegularLabel]): Generated labels based on chain_annotation.
        
    Args:
        chain (Chain): The chain whose attributes will be annotated.
        chain_annotation (Dict[str, bool]): Dictionary mapping attribute names to a flag indicating inclusion.
        font_size (int): Font size to use when rendering labels.
    """
    CHAIN_DEFAULT_ANNOTATION = {'chain_id': True,
                                'algorithm': False,
                                'model_id': True}
    def __init__(self, chain: 'Chain', chain_annotation: Optional[Dict[str, bool]], font_size: int):
        self._chain = chain
        self._chain_annotation = chain_annotation or self.CHAIN_DEFAULT_ANNOTATION
        self._font_size = font_size
        self._labels_storage = self._generate_labels()
    
    
    @property
    def width(self) -> int:
        return max((label.width for label in self._labels_storage), default=0)
    
    @property
    def height(self) -> int:
        start = int(self._font_size * 0.5) * len(self._labels_storage) + 0
        return sum((label.height for label in self._labels_storage), start)
    
    
    def _generate_labels(self) -> RegularLabel:
        """
        Generate RegularLabel instances for each attribute flagged in chain_annotation.

        Iterates over sorted keys of chain_annotation, includes only those set to True.
        Retrieves the attribute value from the chain, defaults to 'N/A' if missing.
        Constructs label text as "<key>: <value>" and creates a RegularLabel.

        Returns:
            List[RegularLabel]: List of generated label objects for rendering.
        """
        labels = []
        for key in sorted(self._chain_annotation.keys()):
            if self._chain_annotation[key]:
                value = getattr(self._chain, key, None)
                if value is None:
                    value = 'N/A'
                text = f"{key}: {value}"
                labels.append(RegularLabel(text, self._font_size, 'DejaVuSans.ttf'))
        return labels
        
    
    def draw(self, draw_context: 'ImageDraw.ImageDraw', y_offset: int):
        """
        Draws all chain labels.

        Args:
            draw_context (ImageDraw.ImageDraw): The PIL drawing context.
            y_offset (int): Vertical offset to start drawing.
        """
        offset = y_offset
        padding = int(self._font_size * 0.5)
        for label in self._labels_storage:
            label.draw(x_0=padding, y_0=offset, draw_context=draw_context)
            offset += label.height + padding
