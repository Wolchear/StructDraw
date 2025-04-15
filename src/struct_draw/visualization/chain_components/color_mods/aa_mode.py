from typing import Dict, Optional

from .base_mode import BaseMode

DEFAULT_HYDROPHILICITY_COLORS = {'hydrophobic': 'red',
                                 'hydrophilic': 'cyan'}

DEFAULT_SINGLE_AA_COLORS = {"A": "#F44336",
                            "R": "#E91E63",
                            "N": "#9C27B0",
                            "D": "#673AB7",
                            "C": "#3F51B5",
                            "E": "#2196F3",
                            "Q": "#03A9F4",
                            "G": "#00BCD4",
                            "H": "#009688",
                            "I": "#4CAF50",
                            "L": "#8BC34A",
                            "K": "#CDDC39",
                            "M": "#FFEB3B",
                            "F": "#FFC107",
                            "P": "#FF9800",
                            "S": "#FF5722",
                            "T": "#795548",
                            "W": "#9E9E9E",
                            "Y": "#607D8B",
                            "V": "#000000"}

AA_GROUPS = {"A": "hydrophobic",  # Alanine
             "R": "hydrophilic",  # Arginine
             "N": "hydrophilic",  # Asparagine
             "D": "hydrophilic",  # Aspartic acid
             "C": "hydrophilic",  # Cysteine
             "E": "hydrophilic",  # Glutamic acid
             "Q": "hydrophilic",  # Glutamine
             "G": "hydrophilic",  # Glycine 
             "H": "hydrophilic",  # Histidine
             "I": "hydrophobic",  # Isoleucine
             "L": "hydrophobic",  # Leucine
             "K": "hydrophilic",  # Lysine
             "M": "hydrophobic",  # Methionine
             "F": "hydrophobic",  # Phenylalanine
             "P": "hydrophobic",  # Proline
             "S": "hydrophilic",  # Serine
             "T": "hydrophilic",  # Threonine
             "W": "hydrophobic",  # Tryptophan
             "Y": "hydrophilic",  # Tyrosine
             "V": "hydrophobic"}  # Valine

class AaMode(BaseMode):
    AVAILABLE_SUB_MODES = ['hydrophilicity', 'single_aa']
    def __init__(self, sub_mode: str, color_palette: Optional[Dict[str, str]] = None):
        super().__init__(sub_mode, self.AVAILABLE_SUB_MODS)
        if color_palette is None:
            if sub_mode == 'hydrophilicity':
                color_palette = DEFAULT_HYDROPHILICITY_COLORS
            elif sub_mode == 'single_aa':
                color_palette = DEFAULT_SINGLE_AA_COLORS
        self.color_palette = color_palette
        
        
    def get_color(self, residue: 'Residue') -> str:
        if self._sub_mode == 'hydrophilicity':
            classification = AA_GROUPS.get(residue.amino_acid)
            if classification is None:
                return "#CCCCCC"
            return self.color_palette.get(classification, "#CCCCCC")
        elif self._sub_mode == 'single_aa':
            return self.color_palette.get(residue.amino_acid, "#CCCCCC")
        return "#CCCCCC"
