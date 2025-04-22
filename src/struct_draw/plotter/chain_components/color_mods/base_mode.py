from abc import ABC, abstractmethod
from typing import Dict, Optional, List

class BaseMode(ABC):
    """
    Abstract base class for defining coloring strategies for chain residues.

    Attributes:
        _sub_mode (str): Selected sub-mode name for the coloring strategy.
    """
    def __init__(self, sub_mode: str, available_sub_mods: List[str]):
        """
        Validate and set the sub-mode for the coloring strategy.

        Args:
            sub_mode (str): Name of the sub-mode to use.
            available_sub_mods (List[str]): List of supported sub-mode names.

        Raises:
            ValueError: If provided sub_mode is not in available_sub_mods.
        """
        self._sub_mode = sub_mode
        if self._sub_mode not in available_sub_mods:
            raise ValueError(f"Unawalable submode: {sub_mode}. Awalable submods: {', '.join(available_sub_mods)}")
        
    @abstractmethod
    def get_color(self, residue: 'Residue') -> str:
        """
        Abstract method to compute a color representation for a given residue.

        Args:
            residue (Residue): The residue object for which the color is determined.

        Returns:
            str: Hex or named color string for rendering the residue.
        """
        pass
