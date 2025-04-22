#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB, PDBx
from struct_draw.structures.alignment import Alignment
from struct_draw.visualization.canvas import Canvas
from struct_draw.visualization import Chain

def run_non_aligned_chains() ->None:
    custom_palette = {'helix': 'red', 'strand': 'green', 'other': 'blue'}
    chain_annotation = {'model_id': False, 'algorithm': False}
    canvas = Canvas('white')
    pdb_file_path = 'tests/alignments/1ad0.pdb'
    dssp_out_path = 'dssp.out'
    with open(dssp_out_path, 'r') as f:
    	dssp_content = f.read()
    pdb = PDB('mkdssp', pdb_file_path)
    chain_A = pdb.get_chain('A')
    canvas.add_chain(Chain(chain_A, shape_size=50, split=80, chain_annotation=chain_annotation, custom_palette=custom_palette))
    
    pdb2 = PDB('mkdssp', pdb_file_path, algorithm_out=dssp_content)
    chain_A2 = pdb2.get_chain('A')
    canvas.add_chain(Chain(chain_A2, shape_size=50, show_amino_code=True, split=80, color_mode='b_factor', color_sub_mode='mean'))
    
    alpha_pdb = PDB('mkdssp','a_predicted.pdb')
    chain_alpha = alpha_pdb.get_chain('A')
    canvas.add_chain(Chain(chain_alpha, shape_size=50, show_amino_code=True, split=80, color_mode='b_factor', color_sub_mode='a_fold'))
    
    alpha_cif = PDBx('mkdssp','a_predicted.cif')
    chain_alpha_cif = alpha_cif.get_chain('A')
    canvas.add_chain(Chain(chain_alpha_cif, shape_size=50, show_amino_code=True, split=80, color_mode='b_factor', color_sub_mode='a_fold'))
    
   
    
    
    #canvas.add_title('DejaVuSans.ttf', 100, 'Test Title', 'right')
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
            canvas.add_chain(Chain(chain_to_add, shape_size=50,show_amino_code=True, split=80, color_mode='b_factor', color_sub_mode='mean'))
    
    img = canvas.get_image()
    img.show()
    
    
def run_struct_draw() -> None:
    run_aligned_chains()

if __name__ == '__main__':
    run_struct_draw()
