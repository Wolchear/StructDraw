import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import numpy as np

from typing import Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from struct_draw.apps.interface import get_algorithm

class BaseModel(ABC):
    def __init__(self, algorithm_name: str, pdb_file: Optional[str] = None, include_only: Optional[list] = None, algorithmm_out: Optional[str] = None):
        self._pdb_file = pdb_file
        self._include_only = include_only
        self._algorithm = get_algorithm(algorithm_name)
        self._algorithmm_out = algorithmm_out if algorithmm_out is not None else self.run_dssp()
        self._chains = self.process_algorithm_data()
        
        
    def get_chain(self, chain_id: str):
        if chain_id not in self._chains:
            raise ValueError(f"File does not contain chain: {chain_id}")
        return self._chains[chain_id]
    
    def get_chain_list(self) -> dict:
        return self._chains
        
    def run_dssp(self) -> str:
        return self._algorithm.run(self._pdb_file)
                                            
    def process_algorithm_data(self) -> dict:
        dssp_data = self._algorithm.process_data(self._algorithmm_out)
        unique_chains = np.unique(dssp_data['chain_id'])
        chains = {}
        for chain_id in unique_chains:
            if self._include_only is not None and chain_id not in self._include_only:
                continue
            chain_data = dssp_data[dssp_data['chain_id'] == chain_id]
            chains[chain_id] = Chain(chain_id, 'mkdssp', self._pdb_file, chain_data)
        return chains

class PDBx(BaseModel):
    def __init__(self, algorithm_name: str, pdb_file: Optional[str] = None, include_only: Optional[list] = None, algorithmm_out: Optional[str] = None):
        super().__init__(algorithm_name, pdb_file, include_only, algorithmm_out)

        
class PDB(BaseModel):   
    def __init__(self, algorithm_name: str, pdb_file: Optional[str] = None, include_only: Optional[list] = None, algorithmm_out: Optional[str] = None):
        super().__init__(algorithm_name, pdb_file, include_only, algorithmm_out)
        
        
@dataclass     
class Chain:
    chain_id: str
    ss_algorithm: str
    model_id: str
    dssp_data: np.ndarray = field(repr=False)
    residues: np.ndarray = field(init=False)
    
    def __post_init__(self):
        self.residues = np.array([
        Residue(index=row['residue_index'],
                insertion_code=row['insertion_code'],
                amino_acid=row['AA'],
                secondary_structure=row['SS'])
        for row in self.dssp_data], dtype=object)
                                           
    def align_seq(self, aligned_seq: str) -> None:
        new_residues = []
        residues_index = 0
        for char in aligned_seq:
            if char != '-':
                new_residues.append(self.residues[residues_index])
                residues_index += 1
            else:
                new_residues.append(Residue(index='-',
                                            insertion_code='-',
                                            amino_acid='_',
                                            secondary_structure='gap'))
        self.residues = np.array(new_residues, dtype=object)
            
@dataclass
class Residue:
	index: int
	insertion_code: str
	amino_acid: str
	secondary_structure: str
