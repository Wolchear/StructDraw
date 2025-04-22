#!/usr/bin/env python3

from struct_draw.structures.alignment import Alignment
from struct_draw.plotter import Chain, Canvas

alignment = 'alignment_data/light.afa'
pdb_files_dir = 'alignment_data/pdb_files'
new_alignment = Alignment(alignment, pdb_files_dir, 'mkdssp')
canvas = Canvas('white')
canvas.add_title('DejaVuSans.ttf', 50, 'Alignment With Custom Palette', 'centered')
NEW_PALETTE = {'helix': 'red',
               'strand': 'green',
               'other': 'grey',
               'gap': 'black'}
for model in new_alignment.models:
    for chain in model.get_chain_list():
        chain_to_add = model.get_chain(chain)
        canvas.add_chain(Chain(chain_to_add, shape_size=50, split=80, color_mode='structure', color_sub_mode='secondary', custom_palette=NEW_PALETTE))
    
img = canvas.get_image()
img.save('alignment_output_image.png')
img.show()
