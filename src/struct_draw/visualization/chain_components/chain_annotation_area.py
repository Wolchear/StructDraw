from typing import Optional, Dict

from .chain_base_area import BaseArea
from struct_draw.visualization.small_units.label import RegularLabel

class AnnotationArea(BaseArea):
    def __init__(self, chain: 'Chain', chain_annotation: Dict[str, bool], font_size: int):
        self._chain = chain
        self._chain_annotation = chain_annotation
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
        offset = y_offset
        padding = int(self._font_size * 0.5)
        for label in self._labels_storage:
            label.draw(x_0=padding, y_0=offset, draw_context=draw_context)
            offset += label.height + padding
