import numpy as np
import plotly.graph_objects as go

from PIL import Image, ImageDraw, ImageFont
from .shapes import Shape

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


def _prepare_chain(chain_data: np.ndarray, res_width:int, res_height:int,
                   x_offset: int = 0, y_offset: int = 0):
                   
    num_residues = len(chain_data)
    
    structures = {'H': 'helix',
                  'I': 'helix',
                  'G': 'helix',
                  'P': 'helix',
                  'B': 'strand',
                  'E': 'strand',
                  'T': 'other',
                  'S': 'other'}
    structure_colors = {'helix': 'green',
                        'strand': 'blue',
                        'other': 'white'}
                        
    index = 1
    shapes = []
    for row in chain_data:
        ss = row['SS']
        aa = row['AA']
        residue_index = row['residue_index']
        insertion_code = row['insertion_code']
        structure = structures.get(ss, 'other')
        fillcolor = structure_colors[structure]
        x0 = x_offset + index * res_width
        y0 = y_offset
        font = ImageFont.load_default()
        shape = Shape(res_width, res_height, residue_index, insertion_code,
                      fillcolor, aa, ss, x0, y0, font, 14)
        
     
        shapes.append(shape)
        index += 1
     
    return shapes

def generate_file_image(pdb_object, res_width:int, res_height:int):
    chain_list = pdb_object.get_chain_list()
    max_len = 0
    file_shapes = []
    for i, chain in enumerate(chain_list):
        chain_data = pdb_object.get_chain(chain)
        shapes = _prepare_chain(chain_data, res_height, res_width, 0, i * res_width + res_width/2)
        current_len = len(chain_data)
        file_shapes.append(shapes)
        if current_len > max_len:
            max_len = current_len
            
    img_width = (max_len + 1) * res_width
    img_height = (res_height + 2 * res_height) * len(chain_list)
    img = Image.new('RGB', (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    for shapes in file_shapes:
        for shape in shapes:
            shape_tuple, font_tuple, info_tuple = shape.get_shape_params()
            coords = shape_tuple[0]
            color = shape_tuple[1]
            outline = shape_tuple[2]
            draw.rectangle(shape_tuple[0], fill=color, outline=outline)
  
    return img	        
        

    
def generate_chain_image(chain_data: np.ndarray, res_width:int, res_height:int):
    num_residues = len(chain_data)
    
    img_width = (num_residues + 1) * res_width
    img_height = res_height + 2 * res_height
    
    shapes = _prepare_chain(chain_data, res_height, res_width)
    img = Image.new('RGB', (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    for shape in shapes:
        shape_tuple, font_tuple, info_tuple = shape.get_shape_params()
        coords = shape_tuple[0]
        color = shape_tuple[1]
        outline = shape_tuple[2]
        draw.rectangle(shape_tuple[0], fill=color, outline=outline)
  
    return img	
