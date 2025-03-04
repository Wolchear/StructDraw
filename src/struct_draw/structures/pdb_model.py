import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import numpy as np

from dataclasses import dataclass
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
            self._chains[chain_id] = Chain(chain_id, 'mkdssp', self._pdb_file,
                                           chain_data['residue_index'],
                                           chain_data['insertion_code'],
                                           chain_data['AA'],
                                           chain_data['SS'])

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
    residue_index: NDArray[np.int_]
    insertion_code: NDArray[np.str_]
    residues: NDArray[np.str_]
    secondary_structure: NDArray[np.str_]
    
if __name__ == '__main__':
   #pdb = PDB('../../../tests/1ad0.pdb')
    pdbx = PDBx('../../../tests/1ad0.cif')
