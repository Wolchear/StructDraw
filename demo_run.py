#!/usr/bin/env python3
import argparse

from struct_draw.structures.pdb_model import PDB
from struct_draw.visualization.canvas import Canvas
from struct_draw.visualization.shapes import Chain

def run_struct_draw(pdb_file_path: str, pdb_file_type: str = None) -> None:
    pdb = PDB(pdb_file_path)
    chain_A = pdb.get_chain_data('A')
    chain_B = pdb.get_chain_data('B')
    canvas = Canvas('white')
    canvas.add_chain(Chain(chain_A, 'struct', shape_size=10, split=80))
    canvas.add_chain(Chain(chain_B, 'struct', shape_size=10))
    canvas.add_title('DejaVuSans.ttf', 50, 'Test Title', 'right')
    #canvas.add_chain(Chain(chain_B, 'struct', 15))
    #canvas.add_chain(Chain(chain_B, 'struct', 20))
    img = canvas.get_image()
    img.show()

if __name__ == '__main__':      
    parser = argparse.ArgumentParser(description="None",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-pdb',
                        type=str,
                        metavar='',
                        required=True,
                        help="PDB/PDBx file")
	
	
    args = parser.parse_args()
	
    run_struct_draw(args.pdb)
