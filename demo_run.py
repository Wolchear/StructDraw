#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB
from struct_draw.structures.alignment import Alignment
from struct_draw.visualization.canvas import Canvas
from struct_draw.visualization import Chain

def run_non_aligned_chains() ->None:
    pdb_file_path = 'tests/alignments/1ad0.pdb'
    dssp_out_path = 'dssp.out'
    with open(dssp_out_path, 'r') as f:
    	dssp_content = f.read()
    pdb = PDB('stride', pdb_file_path)
    pdb2 = PDB('mkdssp', algorithmm_out=dssp_content)
    chain_A = pdb.get_chain('A')
    chain_A2 = pdb2.get_chain('A')
    chain_annotation = {'model_id': True, 'algorithm': True}
    canvas = Canvas('white')
    canvas.add_chain(Chain(chain_A, shape_size=50, split=80, start=150, end=161))
    canvas.add_chain(Chain(chain_A, shape_size=50, split=80, chain_annotation=chain_annotation))
    canvas.add_chain(Chain(chain_A2, shape_size=50, show_amino_code=False, split=80))
    canvas.add_title('DejaVuSans.ttf', 100, 'Test Title', 'right')
    #canvas.add_chain(chain_B, 'struct', shape_size=10)
    img = canvas.get_image()
    img.save('output_image.png')
    img.show()

def run_aligned_chains() -> None:
    alignment = 'tests/alignments/light.afa'
    data_dir = 'tests/alignments'
    new_alignment = Alignment(alignment, data_dir, 'mkdssp')
    canvas = Canvas('white')
    for model in new_alignment.models:
        for chain in model.get_chain_list():
            chain_to_add = model.get_chain(chain)
            canvas.add_chain(Chain(chain_to_add, shape_size=20))
    
    img = canvas.get_image()
    img.show()
    
    
def run_struct_draw() -> None:
    run_aligned_chains()

if __name__ == '__main__':
    run_struct_draw()
