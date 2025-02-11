import subprocess
import re

import numpy as np

class DSSP:
	def __init__(self, pdb_file: str):
		self.pdb_file = pdb_file
		self.dssp_out = self.run_dssp(pdb_file)
		self.dssp_data = self.get_dssp_data(self.dssp_out)
			
	def run_dssp(self, pdb_file: str) -> str:
		DSSP_cmd = ["dssp", "--output-format=dssp", pdb_file]
		p = subprocess.Popen(
			DSSP_cmd,
			universal_newlines=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			)
		out, err = p.communicate()
		
		return out
		
	def get_dssp_data(self, dssp_out: str) -> np.ndarray:
		is_start = False
		data = []
		for line in dssp_out.split('\n'):
			if re.search(r"RESIDUE AA STRUCTURE", line):
				is_start = True
				continue
					
			if not is_start:
				continue
			
			if re.search(r"^$", line):
				continue
			
			if line[11] == ' ': #Skip line if no reidue
				continue
			
			dssp_index = int(line[1:5])
			residue_index = int(line[5:10])
			insertion_code = line[10]
			chain_id = line[11]
			AA = line[13]
			SS = line[16] if line[16] != ' ' else '-'
			data.append((dssp_index, residue_index, insertion_code, chain_id, AA, SS))
		dtype = [
			('dssp_index', 'i4'),
			('residue_index', 'i4'),
			('insertion_code', 'U1'),
			('chain_id', 'U1'),
			('AA', 'U1'),
			('SS', 'U1')
			]
		np_data = np.array(data, dtype=dtype)
		return np_data	
	
	def chain_exists(self, selected_chain: str) -> bool:
		unique_chains = np.unique(self.dssp_data['chain_id'])
		return selected_chain in unique_chains
	
	def get_chain(self, selected_chain: str) -> np.ndarray:
		if not self.chain_exists(selected_chain):
			print(f"Warning: Chain '{selected_chain}' not found.")
			return np.array([])
		return self.dssp_data[self.dssp_data['chain_id'] == selected_chain]





