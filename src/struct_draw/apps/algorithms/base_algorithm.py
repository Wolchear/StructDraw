from abc import ABC, abstractmethod
from typing import Dict, Optional

import numpy as np

class BaseAlgorithm(ABC):
    """
    Abstract base class for secondary‐structure prediction algorithms.

    This class defines a uniform interface for:
      - running a chosen algorithm on a structure file (`run`)
      - post‑processing the algorithm’s raw output into a structured array (`process_data`)

    Attributes
    ----------
    _algorithm_sub_name : str
        Identifier or sub‑name of the specific algorithm implementation.
    _ss_translation : Optional[Dict[str, str]]
        Dictionary for translating secondary‑structure codes (SS_code) into human‑readable labels.
    """
    def __init__(self, algorithm_sub_name: str, ss_translation: Optional[Dict[str,str]]):
        self._algorithm_sub_name = algorithm_sub_name
        self.SS_TRANSLATION = ss_translation
	
    @abstractmethod	
    def run(self, pdb_file: str) -> str:
        """
        Run the selected algorithm on a structure file.

        Parameters
        ----------
        pdb_file : str
            Path to the input structure file. Can be in CIF or PDB format,
            depending on what the algorithm accepts.

        Returns
        -------
        str
            The raw output produced by the algorithm, as a string.
        """
        pass
     
    @abstractmethod  
    def process_data(self, algorithm_out: str) -> np.ndarray:
        """
        Process the raw output of the algorithm into a structured array.

        Parameters
        ----------
        algorithm_out : str
            The result of the algorithm run, passed directly as a string
            (not a file path).

        Returns
        -------
        np.ndarray
            A structured NumPy array with dtype:
            
                dtype = [
                    ('residue_index',   'i4'),
                    ('insertion_code',  'U1'),
                    ('chain_id',        'U1'),
                    ('AA',              'U1'),
                    ('SS',              'U6'),
                    ('SS_code',         'U1')
                ]

            Notes
            -----
            - 'SS_code', 'chain_id' and 'AA' must be extracted from the algorithm output.
            - 'SS' is obtained by mapping 'SS_code' through the provided
              `ss_translation` dictionary.
        """
        pass
