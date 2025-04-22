import os
from typing import List, Dict, Tuple

import numpy as np

from .pdb_model import PDB, PDBx

class Alignment:
    """
    Manages reading of a multi-FASTA alignment file and initialization of PDB models based on that alignment.

    Attributes:
        _alignment_file (str): Path to the FASTA-style alignment file.
        _data_dir (str): Directory containing PDB files referenced in the alignment headers.
        _alignment_data (List[Tuple[str, str]]): List of (header, sequence) pairs from the file.
        models (List[PDB]): Initialized PDB models with aligned sequences.
    """
    def __init__(self, alignment_file: str, data_dir: str, algorithms: str):
        """
        Read the alignment file and create PDB models for each unique entry.

        Args:
            alignment_file (str): FASTA-format alignment file path.
            data_dir (str): Directory where PDB files are stored.
            algorithms (str): Algorithm key used for model initialization.
        """
        self._alignment_file = alignment_file
        self._data_dir = data_dir
        self._alignment_data = self._read_alignment()
        self.models = self._init_models(algorithms)

    def _read_alignment(self) -> List[Tuple[str, str]]:
        """
        Parse the alignment file into header-sequence tuples.

        Returns:
            List[Tuple[str, str]]: A list of (header, sequence) entries.
        """
        models = []
        current_header = None
        current_seq = []
        filepath = self._alignment_file
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if current_header is not None:
                        models.append((current_header, "".join(current_seq)))
                        current_seq = []
                    current_header = line[1:].strip()
                else:
                    current_seq.append(line)
            if current_header is not None:
                models.append((current_header, "".join(current_seq)))
        return models
    
    
    def _init_models(self, algorithms: str) -> List['PDB']:
        """
        Initialize PDB model instances and align sequences based on unique models.

        For each unique (model_id, algorithm) pair:
            1. Construct PDB file path.
            2. Instantiate a PDB object with the algorithm key and chains list.
            3. Align each chain's sequence into the PDB model.

        Returns:
            List[PDB]: List of initialized and sequence-aligned PDB objects.
        """
        
        model_entries = self._get_unique_models()
        new_models: List['PDB'] = []
        for (model_key, file_type), chain_seqs in model_entries.items():
            pdb_file = f"{self._data_dir}/{model_key}.{file_type}"
            chains_list = list(chain_seqs.keys())
            if file_type == 'pdb':
                new_model = PDB(algorithms, pdb_file, chains_list)
            elif file_type == 'cif':
                new_model = PDBx(algorithms, pdb_file, chains_list)
            else:
                continue
            for chain_id, sequence in chain_seqs.items():
                new_model.get_chain(chain_id).align_seq(sequence)
            new_models.append(new_model)
        return new_models
    
    def _get_unique_models(self) -> Dict[Tuple[str, str], Dict[str, str]]:
        """
        Extract unique models and associated chain sequences from alignment headers.

        Parses each header in the alignment data (formatted as 'model|algorithm|chain') and
        groups sequences by (model_id, algorithm_key).

        Returns:
            Dict[Tuple[str, str], Dict[str, str]]: Mapping from (model_id, algorithm_key)
            to a dict of chain_id -> sequence.
        """
        models: Dict[Tuple[str, str], Dict[str, str]] = {}
        for header, seq in self._alignment_data:
            parts = header.split("|")
            if len(parts) < 3:
                continue
            model_key, file_type, chain_id = parts[0], parts[1], parts[2]
            key = (model_key, file_type)
            if key not in models:
                models[key] = {}
            models[key][chain_id] = seq
        return models
