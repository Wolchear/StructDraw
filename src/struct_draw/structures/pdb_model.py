import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import numpy as np

from dataclasses import dataclass, field
from numpy.typing import NDArray
from abc import ABC, abstractmethod
from struct_draw.dssp.dssp import run_dssp, get_dssp_data

class BaseModel(ABC):
    def __init__(self, pdb_file: str):
        self._pdb_file = pdb_file
        self._file_type = BaseModel.identify_file_type(pdb_file)
        self._chains = {}
        self._unique_chains = None
        self._dssp_out = None
        
    @staticmethod
    def validate_file_type(pdb_file: str, expected: str) -> None:
        actual = BaseModel.identify_file_type(pdb_file)
        if actual != expected:
            raise ValueError(f"File type mismatch: expected '{expected}', got '{actual}'")
    
    @staticmethod
    def identify_file_type(pdb_file: str) -> str:
        try:
            with open( pdb_file, 'r') as file:
                for line in file:
                    if '_data' in line:
                        return 'pdbx'
            return 'pdb'
			
        except OSError as e:
            raise OSError(f"Cannot read file ({pdb_file}): {e}")
    
    
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
            chain_data = dssp_data[dssp_data['chain_id'] == chain_id]
            self._chains[chain_id] = Chain(chain_id, 'mkdssp',
                                           self._pdb_file,
                                           chain_data)

class PDBx(BaseModel):
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        BaseModel.validate_file_type(self._pdb_file, 'pdbx')
        self.run_dssp()

        
class PDB(BaseModel):   
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        BaseModel.validate_file_type(self._pdb_file, 'pdb')
        self.run_dssp()
        
        
@dataclass     
class Chain:
    chain_id: str
    ss_algorithm: str
    model_id: str
    dssp_data: np.ndarray = field(repr=False)
    residues: np.ndarray = field(init=False)
    
    def __post_init__(self):
        self.residues = np.empty(len(self.dssp_data), dtype=object)
        for index, row in enumerate(self.dssp_data):
            self.residues[index] = Residue(index=row['residue_index'],
                                           insertion_code=row['insertion_code'],
                                           amino_acid=row['AA'],
                                           secondary_structure=row['SS'])
    	
@dataclass
class Residue:
	index: int
	insertion_code: str
	amino_acid: str
	secondary_structure: str
