import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx

def identify_file_type(pdb_file: str) -> str:
	try:
		with open( pdb_file, 'r') as file:
			for line in file:
				if '_data' in line:
					return 'cif'
			return 'pdb'
			
	except Exception as e:
		print(f"File ({file_name}) reading error: {e}")
		raise
	
	
def read_file(pdb_file_path: str, pdb_file_type: str):
	if pdb_file_type == 'pdb':
		pdb_file = pdb.PDBFile.read(pdb_file_path)
		return pdb_file.get_structure()
	else:
		cif_file = pdbx.CIFFile.read(pdb_file_path)
		return cif_file
