import os
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict
import re

import numpy as np

class BaseModel(ABC):
    """
    Abstract base class for running structural analysis algorithms (e.g., DSSP) on PDB files
    and converting the output into Chain objects.

    Attributes:
        _pdb_file (Optional[str]): Path to the PDB file to analyze.
        _include_only (Optional[list]): List of chain IDs to include in the output; None means all.
        _algorithm (Object): Instance of the algorithm handler obtained via get_algorithm.
        _algorithm_out (str): Raw output from the algorithm run or provided path to processed data.
        _chains (dict): Mapping of chain IDs to Chain instances created from algorithm data.
    """
    def __init__(
        self, algorithm, pdb_file: Optional[str] = None,
        include_only: Optional[list] = None, algorithm_out: Optional[str] = None
        ):
        """
        Initialize the BaseModel with algorithm settings and process the structural data.

        Args:
            algorithm (object): Algorithm object.
            pdb_file (Optional[str]): Path to the input PDB file.
            include_only (Optional[list]): Chain IDs to include in final output.
            algorithm_out (Optional[str]): Precomputed algorithm output path or data.
        """
        self._pdb_file = pdb_file
        self._include_only = include_only
        self._algorithm = algorithm
        self._algorithm_out = algorithm_out if algorithm_out is not None else self.run_algorithm()
        self._chains = self.process_algorithm_data()
        
        
    def get_chain(self, chain_id: str):
        """
        Retrieve a specific Chain instance by its ID.

        Args:
            chain_id (str): Identifier of the chain to retrieve.

        Returns:
            Chain: The Chain object corresponding to the ID.

        Raises:
            ValueError: If the requested chain ID is not found.
        """
        if chain_id not in self._chains:
            raise ValueError(f"File does not contain chain: {chain_id}")
        return self._chains[chain_id]
    
    def get_chain_list(self) -> dict:
        return self._chains
        
    def run_algorithm(self) -> str:
        return self._algorithm.run(self._pdb_file)
                                            
    def process_algorithm_data(self) -> dict:
        """
        Parse the algorithm output and construct Chain objects for each chain.

        Process:
            1. Load algorithm data into a DataFrame (expects 'chain_id' column).
            2. Identify unique chain IDs.
            3. Filter by include_only if set.
            4. Create a Chain object for each chain present.

        Returns:
            dict: Mapping from chain IDs to Chain instances.
        """
        dssp_data = self._algorithm.process_data(self._algorithm_out)
        unique_chains = np.unique(dssp_data['chain_id'])
        chains = {}
        for chain_id in unique_chains:
            if self._include_only is not None and chain_id not in self._include_only:
                continue
            chain_data = dssp_data[dssp_data['chain_id'] == chain_id]
            pdb_id = None
            if self._pdb_file is not None:
                pdb_id = os.path.splitext(os.path.basename(self._pdb_file))[0]
            chains[chain_id] = Chain(chain_id, str(self._algorithm), pdb_id, chain_data)
        return chains
    
    @abstractmethod   
    def parse_b_factor(self) -> None:
        """
        Abstract method to parse or process B-factor values for residues.

        Implementations should populate or modify feature data related to residue flexibility.
        """
        pass

class PDBx(BaseModel):
    def __init__(self, algorithm: str, pdb_file: Optional[str] = None, include_only: Optional[list] = None, algorithm_out: Optional[str] = None):
        super().__init__(algorithm, pdb_file, include_only, algorithm_out)
        if self._pdb_file is not None:
            self.parse_b_factor()
            
    def parse_b_factor(self) -> None:
        bf_raw: Dict[Tuple[str, int, str], List[float]] = defaultdict(list)
        in_loop = False
        headers: List[str] = []
        idx_map: Dict[str, int] = {}
        wanted = {'label_asym_id',
                  'label_seq_id',
                  'pdbx_PDB_ins_code',
                  'B_iso_or_equiv'}
        with open(self._pdb_file, 'r') as fh:
            for line in fh:
                line = line.strip()
                if line.startswith('loop_'):
                    in_loop = True
                    headers.clear()
                    idx_map.clear()
                    continue
                if in_loop and line.startswith('_atom_site.'):
                    tag = line.split('.', 1)[1]
                    headers.append(tag)
                    continue
                if in_loop and headers and not line.startswith('_atom_site.') and line:
                    if not idx_map:
                        for i, tag in enumerate(headers):
                            if tag in wanted:
                                idx_map[tag] = i
                    parts = re.split(r"\s+", line)
                    try:
                        chain = parts[idx_map['label_asym_id']]
                        res_seq = int(parts[idx_map['label_seq_id']])
                        ins_code = parts[idx_map['pdbx_PDB_ins_code']]
                        if ins_code == '?':
                            ins_code = ' '
                        b_val = float(parts[idx_map['B_iso_or_equiv']])
                    except (KeyError, ValueError, IndexError):
                        continue
                    bf_raw[(chain, res_seq, ins_code)].append(b_val)
                if in_loop and headers and not line:
                    in_loop = False
        bf_vec = {k: np.array(v, dtype=float) for k, v in bf_raw.items()}
        for chain in self._chains.values():
            for res in chain.residues:
                key = (chain.chain_id, res.index, res.insertion_code)
                res.b_factors = bf_vec.get(key, np.array([], dtype=float))
        
        
class PDB(BaseModel):   
    def __init__(self, algorithm: str, pdb_file: Optional[str] = None, include_only: Optional[list] = None, algorithm_out: Optional[str] = None):
        super().__init__(algorithm, pdb_file, include_only, algorithm_out)
        if self._pdb_file is not None:
            self.parse_b_factor()
    
    
    def parse_b_factor(self) -> None:
        bf_raw = defaultdict(list)
        b_pattern = re.compile(r'^\d+\.\d{2}$')
        with open(self._pdb_file, 'r') as fh:
            for line in fh:
                if not line.startswith('ATOM'):
                    continue
                chain_id = line[21].strip()
                seq_str = line[22:26].strip()
                if not seq_str.isdigit():
                    continue
                res_seq = int(seq_str)
                ins_code = line[26].strip() or ' '
                b_str = line[60:66].strip()
                if not b_pattern.match(b_str):
                    continue
                b_val = float(b_str)
                bf_raw[(chain_id, res_seq, ins_code)].append(b_val)
        bf_vec = {k: np.array(v, dtype=float) for k, v in bf_raw.items()}
        for chain in self._chains.values():
            for res in chain.residues:
                key = (chain.chain_id, res.index, res.insertion_code)
                res.b_factors = bf_vec.get(key, np.array([], dtype=float))
                
        
@dataclass     
class Chain:
    chain_id: str
    algorithm: str
    model_id: str
    dssp_data: np.ndarray = field(repr=False)
    residues: np.ndarray = field(init=False)
    
    def __post_init__(self):
        self.residues = np.array([
        Residue(index=row['residue_index'],
                insertion_code=row['insertion_code'],
                amino_acid=row['AA'],
                secondary_structure=row['SS'],
                ss_code=row['SS_code'])
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
                                            insertion_code=' ',
                                            amino_acid='',
                                            secondary_structure='gap',
                                            ss_code='-'))
        self.residues = np.array(new_residues, dtype=object)
            
@dataclass
class Residue:
	index: int
	insertion_code: str
	amino_acid: str
	secondary_structure: str
	ss_code: str
	b_factors: np.ndarray = field(default_factory=lambda: np.array([], dtype=float))
