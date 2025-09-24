from struct_draw.structures.pdb_model import PDB, PDBx
from struct_draw.plotter import Chain, Canvas

data_dir = 'data/'

pdb_file = data_dir + '1ad0.pdb'
predicted_pdb_file = data_dir + '1ad0_predicted.cif'


canvas = Canvas('white')
canvas.add_title(font='DejaVuSans.ttf', font_size=50, text='True and Predicted Chains Comparison', text_position='centered')

pdb_model = PDB(algorithm_name='mkdssp', pdb_file=pdb_file)
chain_A = pdb_model.get_chain('A')
canvas.add_chain(Chain(chain_A, shape_size=50, split=80, color_mode='b_factor', color_sub_mode='mean'))

predicted_model = PDBx('mkdssp', predicted_pdb_file)
predicted_chain_A = predicted_model.get_chain('A')
canvas.add_chain(Chain(predicted_chain_A, shape_size=50, split=80, color_mode='b_factor', color_sub_mode='a_fold'))

img = canvas.get_image()
img.save('output_image.png')
img.show()
