import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import numpy as np

from abc import ABC, abstractmethod
from struct_draw.dssp.dssp import run_dssp, get_dssp_data

class Model(ABC):
    def __init__(self, pdb_file: str):
        self._pdb_file = pdb_file
        self._file_type = Model.identify_file_type(pdb_file)
        self._chains = {}
    
    @staticmethod
    def validate_file_type(pdb_file: str, expected: str) -> None:
        actual = Model.identify_file_type(pdb_file)
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
    
    @abstractmethod
    def read_file(self):
        pass
    
    @abstractmethod
    def get_chain_data(self, chain_id: str):
        pass
    
    @abstractmethod
    def get_chain_list(self):
        pass
        

class PDBx(Model):
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        Model.validate_file_type(self._pdb_file, 'pdbx')
        
       	dssp_out = run_dssp(self._pdb_file)
        dssp_data = get_dssp_data(dssp_out)
        
        self.__unique_chains = np.unique(dssp_data['chain_id'])
       
        for chain_id in self.__unique_chains:
             self._chains[chain_id] = dssp_data[dssp_data['chain_id'] == chain_id]
        
    def read_file(self):
        pdbx_file = pdbx.CIFFile.read(self._pdb_file) 
        return pdbx.get_structure(pdbx_file, model=1)
        
    def get_chain_data(self, chain_id: str):
        if chain_id not in self.__unique_chains:
            raise ValueError(f"File do not contains chain: {chain_id}'")
        return self._chains[chain_id]
          
    def get_chain_list(self):
        return self._chains
        
        
class PDB(Model):   
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        Model.validate_file_type(self._pdb_file, 'pdb')
        
        dssp_out = run_dssp(self._pdb_file)
        dssp_data = get_dssp_data(dssp_out)
        
        self.__unique_chains = np.unique(dssp_data['chain_id'])
        
        for chain_id in self.__unique_chains:
             self._chains[chain_id] = dssp_data[dssp_data['chain_id'] == chain_id]
        
    
    def read_file(self):
        pdb_file = pdb.PDBFile.read(self._pdb_file)
        return pdb_file.get_structure()
    
    def get_chain_data(self, chain_id: str):
        if chain_id not in self.__unique_chains:
            raise ValueError(f"File do not contains chain: {chain_id}'")
        return self._chains[chain_id]
        
    def get_chain_list(self):
        return self._chains
        
if __name__ == '__main__':
   #pdb = PDB('../../../tests/1ad0.pdb')
    pdbx = PDBx('../../../tests/1ad0.cif')
