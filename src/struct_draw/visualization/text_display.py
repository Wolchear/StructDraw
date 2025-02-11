import numpy as np

def generate_dssp_text(chain_data: np.ndarray) -> str:
	output = "chain_id residue_id insertion_code aa ss\n"
	for row in chain_data:
		chain_id = row['chain_id']
		residue_id = row['residue_index']
		insertion_code = row['insertion_code']
		aa = row['AA']
		ss = row['SS']
        
		output += f"{chain_id}\t{residue_id}{insertion_code}\t{aa}\t{ss}\n"
    
	return output
