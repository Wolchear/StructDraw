#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB, PDBx
from struct_draw.structures.alignment import Alignment
from struct_draw.visualization.canvas import Canvas
from struct_draw.visualization import Chain


def run_non_aligned_chains() -> None:
    canvas = Canvas('white')
    pdb = PDB('mkdssp', '1mbn.pdb')
    chain_A = pdb.get_chain('A')
    canvas.add_chain(Chain(chain_A, shape_size=50, split=80, color_mode='b_factor', color_sub_mode='mean'))
    
    cif = PDBx('mkdssp', '1mbn.cif')
    chain_A_cif = cif.get_chain('A')
    canvas.add_chain(Chain(chain_A_cif, shape_size=50, split=80, color_mode='b_factor', color_sub_mode='mean'))
    
    cif_predicted = PDBx('mkdssp', '1mbn_predicted.cif')
    chain_A_cif_predicted = cif_predicted.get_chain('A')
    canvas.add_chain(Chain(chain_A_cif_predicted,shape_size=50, split=80, color_mode='b_factor', color_sub_mode='a_fold'))
    
    img = canvas.get_image()
    img.show()
    
    
def run_struct_draw() -> None:
    run_non_aligned_chains()

if __name__ == '__main__':
    run_struct_draw()
