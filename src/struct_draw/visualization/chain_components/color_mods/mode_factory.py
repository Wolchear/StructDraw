from typing import Dict, Optional
from .structure_mode import StructureMode
from .aa_mode import AaMode
from .base_mode import BaseMode

AVAILABLE_MODS = ['structure', 'aa']
def create_mode( mode_type: str, sub_mode: str, 
    color_palette: Optional[Dict[str, str]] = None) -> BaseMode:
    mode_type_lower = mode_type.lower()
    if mode_type_lower == "structure":
        return StructureMode(sub_mode, color_palette)
    elif mode_type_lower == "aa":
        return AaMode(sub_mode, color_palette)
    else:
        raise ValueError(f"Wrong coloring mode: {mode_type}. Available mods: {', '.join(available_sub_mods)}")

