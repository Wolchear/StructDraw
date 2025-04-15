from abc import ABC, abstractmethod

class BaseArea(ABC):
    def __init__(self):
        pass
        
    @property
    @abstractmethod
    def width(self) -> int:
        pass
    
    @property
    @abstractmethod
    def height(self) -> int:
        pass
    
    @abstractmethod
    def draw(self, draw_context: 'ImageDraw.ImageDraw', offset: int) -> None:
        pass
