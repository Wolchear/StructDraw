import numpy as np
import plotly.graph_objects as go

from .shapes import Chain
from .canvas import Canvas

def generate_dssp_text(chain_data: np.ndarray) -> str:
    output = "chain_id residue_id insertion_code aa ss\n"
    for row in chain_data:
        chain_id = row['chain_id']
        residue_id = row['residue_index']
        insertion_code = row['insertion_code']
        aa = row['AA']
        ss = row['SS']
        
    output += f"{chain_id}\t{residue_id}{insertion_code}\t{aa}\t{ss}\n"
    
    return output

def generate_file_image(pdb_object, res_width:int, res_height:int):
    canvas = Canvas('white', None, 12)
    chains_to_visualaize = []
    for chain_id in pdb_object.get_chain_list():
        chain_data = pdb_object.get_chain_data(chain_id)
        chain = Chain(chain_data, 'structures')
        canvas.add_chain(chain)
            
    img = canvas.get_image()
    return img       
        

def generate_chain_image(chain_data: np.ndarray, res_width:int, res_height:int):
    canvas = Canvas('white', None, 12)
    chain = Chain(chain_data, 'structures')
    canvas.add_chain(chain)
    
    img = canvas.get_image()
    return img	
