import subprocess
import re
from typing import Dict, Optional

import numpy as np

from .base_algorithm import BaseAlgorithm


DEFAULT_SS_TRANSLATION = {'H': 'Helix',
                          'G': 'Helix',
                          'I': 'Helix',
                          'E': 'Strand',
                          'B': 'Strand',
                          'T': 'Other',
                          'S': 'Other'}


class DSSP(BaseAlgorithm):
    def __init__(self, algorithm_sub_name: str, ss_translation: Optional[Dict[str,str]]):
        super().__init__(algorithm_sub_name, ss_translation)
        if self.SS_TRANSLATION is None:
            self.SS_TRANSLATION = DEFAULT_SS_TRANSLATION
        
    
    def run(self, pdb_file: str) -> str:
        command = [self._algorithm_sub_name, "--output-format=dssp", pdb_file]
        p = subprocess.Popen(command, universal_newlines=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                         
        out, err = p.communicate()
        return out
        
    def process_data(self, algorithm_out: str) -> np.ndarray:
        is_start = False
        data = []
        for line in algorithm_out.split('\n'):
            if re.search(r"RESIDUE AA STRUCTURE", line):
                is_start = True
                continue
					    
            if not is_start:
                continue
			    
            if re.search(r"^$", line):
                continue
			    
            if line[11] == ' ': #Skip line if no reidue
                continue
	    
            residue_index = int(line[5:10])
            insertion_code = line[10]
            chain_id = line[11]
            AA = line[13]
            SS_code = line[16] if line[16] != ' ' else '-'
            SS = self.SS_TRANSLATION.get(SS_code, 'Other')
            data.append((residue_index, insertion_code, chain_id, AA, SS, SS_code))
            
        dtype = [('residue_index', 'i4'),
                ('insertion_code', 'U1'),
                ('chain_id', 'U1'),
                ('AA', 'U1'),
                ('SS', 'U6'),
                ('SS_code', 'U1')]
        np_data = np.array(data, dtype=dtype)
        return np_data
