import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx

from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, pdb_file: str):
        self._pdb_file = pdb_file
        self._chains = []
        self._file_type = Model.identify_file_type(pdb_file)
    
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
			
        except Exception as e:
            print(f"File ({pdb_file}) reading error: {e}")
            raise
    
    @abstractmethod
    def read_file(self):
        pass
        

class PDBx(Model):
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        Model.validate_file_type(self._pdb_file, 'pdbx')
        self._structure = self.read_file()
        
    def read_file(self):
        pdbx_file = pdbx.CIFFile.read(self._pdb_file) 
        return pdbx.get_structure(pdbx_file, model=1)
        
class PDB(Model):   
    def __init__(self, pdb_file: str):
        super().__init__(pdb_file)
        Model.validate_file_type(self._pdb_file, 'pdb')
        self._structure = self.read_file()
    
    def read_file(self):
        pdb_file = pdb.PDBFile.read(self._pdb_file)
        return pdb_file.get_structure()    
