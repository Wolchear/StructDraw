from abc import ABC, abstractmethod
from typing import Optional

class BaseCanvasComponent(ABC):
    def __init__(self):
        self._width = 0
        self._height = 0
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def width(self) -> int:
        return self._width

    @abstractmethod
    def compute_size(self, canvas_width: Optional[int] = None) -> None:
        pass
    
    @abstractmethod
    def draw(self) -> None:
        pass
