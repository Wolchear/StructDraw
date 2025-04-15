from .base_component import BaseCanvasComponent
from struct_draw.visualization.chain import Chain

class DrawArea(BaseCanvasComponent):
    def __init__(self):
        super().__init__()
        self.__chains_storage = []
        
    def add_chain(self, chain: 'Chain', shape_size, show_amino_code, split, start, end, chain_annotation) -> None:
        new_chain = Chain(chain, 'struct', shape_size,show_amino_code, split, start, end, chain_annotation)
        self.__chains_storage.append(new_chain)
    
    def compute_size(self) -> None:
        self._height = sum(chain.height for chain in self.__chains_storage)
        self._width = max((chain.width for chain in self.__chains_storage), default=0)
        
    def draw(self, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
    	y_offset = offset
    	x_offset = max((chain.annotation_area.width for chain in self.__chains_storage), default=0)
    	for chain in self.__chains_storage:
    		chain.draw(draw_context, y_offset, x_offset)
    		y_offset += chain.height
