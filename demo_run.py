#!/usr/bin/env python3
import argparse

from struct_draw.dssp.dssp import DSSP
from struct_draw.io import file_reader as fr
from struct_draw.visualization.text_display import generate_dssp_text


def run_struct_draw(pdb_file_path: str, pdb_file_type: str = None) -> None:
	#if pdb_file_type is None:
	#	pdb_file_type = fr.identify_file_type(pdb_file_path)
	
	#structure = fr.read_file(pdb_file_path, pdb_file_type)
	
	dssp = DSSP(pdb_file_path)
	chain_A = dssp.get_chain('A')
	print(generate_dssp_text(chain_A))


if __name__ == '__main__':      
	parser = argparse.ArgumentParser(description="None", formatter_class=argparse.RawTextHelpFormatter)
	
	parser.add_argument(
			'-pdb',
			type=str,
			metavar='',
			required=True,
			help="PDB/PDBx file")
	
	parser.add_argument(
			'-pdb_type',
			type=str,
			metavar='',
			required=False,
			help="Enter pdb or cif")
	
	args = parser.parse_args()
	
	run_struct_draw(args.pdb, args.pdb_type)
