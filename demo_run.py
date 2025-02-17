#!/usr/bin/env python3
import argparse

from struct_draw.structures.pdb_model import PDB
from struct_draw.visualization.visualisation import  generate_chain_image, generate_file_image

def run_struct_draw(pdb_file_path: str, pdb_file_type: str = None) -> None:
    pdb = PDB(pdb_file_path)
    chain_A = pdb.get_chain('A')
    chain_B = pdb.get_chain('B')
    fig = generate_file_image(pdb, 10, 10)
    fig.show()

if __name__ == '__main__':      
    parser = argparse.ArgumentParser(description="None", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-pdb',
                        type=str,
                        metavar='',
                        required=True,
                        help="PDB/PDBx file")
	
	
    args = parser.parse_args()
	
    run_struct_draw(args.pdb)
