from typing import Dict, Optional

from .base_mode import BaseMode

STRUCTURES_GROUPS = { 'H': 'Helix', 'I': 'Helix', 'G': 'Helix', 'P': 'Helix',
                      'B': 'Strand', 'E': 'Strand',
                      'T': 'Other', 'S': 'Other','-': 'Other', 'C': 'Other',
                      'gap': 'Gap'}
                      
DEFAULT_STRUCTURES_COLORS = {'Helix': 'green',
                             'Strand': 'blue',
                             'Other': 'white',
                             'Gap': 'black'}

class StructureMode(BaseMode):
    AVAILABLE_SUB_MODS = ['secondary']
    def __init__(self, sub_mode: str, color_palette: Optional[Dict[str, str]] = None):
        super().__init__(sub_mode, self.AVAILABLE_SUB_MODS)
        if color_palette is None:
            if sub_mode == 'secondary':
                color_palette = DEFAULT_STRUCTURES_COLORS
        self.color_palette = color_palette
        
        
    def get_color(self, residue: 'Residue') -> str:
        if self._sub_mode == 'secondary':
            classification = STRUCTURES_GROUPS.get(residue.secondary_structure)
            if classification is None:
                return "#CCCCCC"
            return self.color_palette.get(classification, "#CCCCCC")
        return "#CCCCCC"
