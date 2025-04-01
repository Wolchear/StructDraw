import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import numpy as np

from typing import Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from struct_draw.dssp.dssp import run_dssp, get_dssp_data

class BaseModel(ABC):
    def __init__(self, pdb_file: str, include_chains: Optional[list] = 'ALL'):
        self._pdb_file = pdb_file
        self._chains = {}
        self._unique_chains = None
        self._dssp_out = None
        self._include_chains = include_chains
    
    
    def get_chain(self, chain_id: str):
        if chain_id not in self._unique_chains:
            raise ValueError(f"File do not contains chain: {chain_id}'")
        return self._chains[chain_id]
    
    def get_chain_list(self):
        return self._chains
        
    def run_dssp(self):
        self._dssp_out = run_dssp(self._pdb_file)
        dssp_data = get_dssp_data(self._dssp_out)
        self._unique_chains = np.unique(dssp_data['chain_id'])
        for chain_id in self._unique_chains:
            if self._include_chains != 'ALL' and chain_id not in self._include_chains:
                continue
            chain_data = dssp_data[dssp_data['chain_id'] == chain_id]
            self._chains[chain_id] = Chain(chain_id, 'mkdssp',
                                           self._pdb_file,
                                           chain_data)

class PDBx(BaseModel):
    def __init__(self, pdb_file: str, include_chains: Optional[list] = 'ALL'):
        super().__init__(pdb_file, include_chains)
        self.run_dssp()

        
class PDB(BaseModel):   
    def __init__(self, pdb_file: str, include_chains: Optional[list] = 'ALL'):
        super().__init__(pdb_file, include_chains)
        self.run_dssp()
        
        
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
