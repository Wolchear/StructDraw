import os

import numpy as np

from .pdb_model import PDB, PDBx

class Alignment:
    def __init__(self, alignment_file: str, data_dir: str, algorithms: str):
        self._alignment_file = alignment_file
        self._data_dir = data_dir
        self._alignment_data = self._read_alignment()
        self.models = self._init_models(algorithms)

    def _read_alignment(self):
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
    
    
    def _init_models(self, algorithms: str):
        models = self._get_unique_models()
        new_models = []
        for model_id, chains in models.items():
            pdb_file = self._data_dir + '/' +model_id
            chains_list = [chain_id for d in chains for chain_id in d.keys()]
            new_model = PDB(algorithms, pdb_file, chains_list)
            for chain_dict in chains:
                for chain_id, sequence in chain_dict.items():
                    new_chain = new_model.get_chain(chain_id)
                    new_chain.align_seq(sequence)
            
            new_models.append(new_model)
        return new_models
    
    def _get_unique_models(self):
        models = {}
        for header, seq in self._alignment_data:
            parts = header.split("|")
            if len(parts) < 3:
                continue
            model_id = parts[0] + '.' + parts[1]
            chain_id = parts[2]
            if model_id not in models:
                models[model_id] = []
            models[model_id].append({chain_id: seq})
        return models
