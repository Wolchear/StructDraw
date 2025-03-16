#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB
from struct_draw.visualization.canvas import Canvas

def run_struct_draw() -> None:
    pdb_file_path = 'tests/1ad0.pdb'
    pdb = PDB(pdb_file_path)
    chain_A = pdb.get_chain('A')
    chain_B = pdb.get_chain('B')
    canvas = Canvas('white')
    annotate_dict = {'secondary_structure': True}
    annotate_dict_2 = {'secondary_structure': True, 'amino_acid': True}
    canvas.add_chain(chain_A, shape_size=20, annotate=annotate_dict)
    canvas.add_chain(chain_A, shape_size=20, annotate=annotate_dict_2, split=80)
    #canvas.add_title('DejaVuSans.ttf', 50, 'Test Title', 'right')
    #canvas.add_chain(chain_B, 'struct', shape_size=10)
    img = canvas.get_image()
    img.show()

if __name__ == '__main__':
    run_struct_draw()
