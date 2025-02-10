from . import file_reader as fr
from .dssp import DSSP

def run_struct_draw(pdb_file_path: str, pdb_file_type: str = None) -> None:
	if pdb_file_type is None:
		pdb_file_type = fr.identify_file_type(pdb_file_path)
	
	structure = fr.read_file(pdb_file_path, pdb_file_type)
	
	dssp = DSSP(pdb_file_path)
	print(dssp.np_data)
	
	
	
