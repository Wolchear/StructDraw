from abc import ABC, abstractmethod
from typing import Dict, Optional, List

class BaseMode(ABC):
    def __init__(self, sub_mode: str, available_sub_mods: List[str]):
        self._sub_mode = sub_mode
        if self._sub_mode not in available_sub_mods:
            raise ValueError(f"Unawalable submode: {sub_mode}. Awalable submods: {', '.join(available_sub_mods)}")
        
    @abstractmethod
    def get_color(self, residue: 'Residue') -> str:
        pass
