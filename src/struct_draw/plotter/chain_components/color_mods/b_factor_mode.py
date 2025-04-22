from typing import Dict, Optional

import numpy as np

from .base_mode import BaseMode

class bFactorMode(BaseMode):
    AVAILABLE_SUB_MODS = ['mean', 'median', 'lowest', 'highest', 'a_fold']
    DEFAULT_ALPHA_FOLD = {(0, 20):   '#FF0000',  # red
                          (20, 50):  '#FF7F00',  # orange
                          (50, 70):  '#FFFF00',  # yellow
                          (70, 90):  '#ADD8E6',  # lightblue
                          (90, 100): '#0000FF'}  # blue
                          
    DEFAULT_PALETTE = {(0,   20):  '#0000FF',  # blue
                       (20,  40):  '#00FFFF',  # cyan
                       (40,  60):  '#00FF00',  # green
                       (60,  80):  '#FFFF00',  # yellow
                       (80, 200):  '#FF0000'}  # red 
    OPS = {'mean': np.mean,
           'median': np.median,
           'lowest': np.min,
           'highest':np.max,
           'a_fold': np.min} 
    def __init__(self, sub_mode: str, color_palette: Optional[Dict[str, str]] = None):
        super().__init__(sub_mode, self.AVAILABLE_SUB_MODS)
        if color_palette is None:
            if self._sub_mode != 'a_fold':
                self.palette = self.DEFAULT_PALETTE
            else:
                self.palette = self.DEFAULT_ALPHA_FOLD
        else:
            self.palette = color_palette
        
        
    def get_color(self, residue: 'Residue') -> str:
        b_value = self._get_num_from_vector(residue.b_factors)
        for (low, high), color in self.palette.items():
            if low <= b_value <= high:
                return color
        return "#CCCCCC"
        
    
    def _get_num_from_vector(self, b_vector: np.ndarray) -> float:
        if b_vector.size == 0:
            return 0.0
        return float(self.OPS[self._sub_mode](b_vector))
            
