import subprocess
import re

import numpy as np

from .base_algorithm import BaseAlgorithm


AMINO_ACIDS = { "ALA": "A",
                "ARG": "R",
                "ASN": "N",
                "ASP": "D",
                "CYS": "C",
                "GLN": "Q",
                "GLU": "E",
                "GLY": "G",
                "HIS": "H",
                "ILE": "I",
                "LEU": "L",
                "LYS": "K",
                "MET": "M",
                "PHE": "F",
                "PRO": "P",
                "SER": "S",
                "THR": "T",
                "TRP": "W",
                "TYR": "Y",
                "VAL": "V" }


class Stride(BaseAlgorithm):
    def __init__(self, algorithm_sub_name: str):
        super().__init__(algorithm_sub_name)
        
    
    def run(self, pdb_file: str) -> str:
        command = [self._algorithm_sub_name, pdb_file]
        p = subprocess.Popen(command, universal_newlines=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                         
        out, err = p.communicate()
        return out
        
    def process_data(self, algorithm_out: str) -> np.ndarray:
        data = []
        for line in algorithm_out.split('\n'):
            if not re.search(r"^ASG", line):
                continue
			
            residue_index_with_insertion_code = line[10:15]
            residue_index_with_insertion_code = residue_index_with_insertion_code.replace(" ", "")
            if not residue_index_with_insertion_code[-1].isdigit():
                insertion_code = residue_index_with_insertion_code[-1]
                residue_index = int(residue_index_with_insertion_code[:-1])
            else:
                insertion_code = ""
                residue_index = int(residue_index_with_insertion_code)
            chain_id = line[9]
            AA = AMINO_ACIDS.get(line[5:7], 'X')
            SS = line[24]
            data.append((residue_index, insertion_code, chain_id, AA, SS))
            
        dtype = [('residue_index', 'i4'),
                ('insertion_code', 'U1'),
                ('chain_id', 'U1'),
                ('AA', 'U1'),
                ('SS', 'U1')]
			    
        np_data = np.array(data, dtype=dtype)
        return np_data
