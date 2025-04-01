#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB
from struct_draw.structures.alignment import Alignment
from struct_draw.visualization.canvas import Canvas


def run_non_aligned_chains() ->None:
    pdb_file_path = 'tests/alignments/1ad0.pdb'
    pdb = PDB(pdb_file_path)
    chain_A = pdb.get_chain('A')
    chain_B = pdb.get_chain('B')
    canvas = Canvas('white')
    annotate_dict = {'secondary_structure': True}
    annotate_dict_2 = {'secondary_structure': True, 'amino_acid': True}
    canvas.add_chain(chain_A, shape_size=50, annotate=None)
    canvas.add_chain(chain_A, shape_size=50, annotate=annotate_dict_2, split=80)
    canvas.add_title('DejaVuSans.ttf', 100, 'Test Title', 'right')
    #canvas.add_chain(chain_B, 'struct', shape_size=10)
    img = canvas.get_image()
    img.show()

def run_aligned_chains() -> None:
    alignment = 'tests/alignments/light.afa'
    data_dir = 'tests/alignments'
    new_alignment = Alignment(alignment, data_dir)
    canvas = Canvas('white')
    annotate_dict = {'secondary_structure': True}
    for model in new_alignment.models:
        for chain in model.get_chain_list():
            chain_to_add = model.get_chain(chain)
            canvas.add_chain(chain_to_add, shape_size=20,annotate=annotate_dict)
    
    img = canvas.get_image()
    img.show()
    
    
def run_struct_draw() -> None:
    run_non_aligned_chains()

if __name__ == '__main__':
    run_struct_draw()
