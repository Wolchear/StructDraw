import numpy as np
import plotly.graph_objects as go
import pandas as pd

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
	
	
def generate_dssp_image(chain_data: np.ndarray):
	structures = {'H': 'helix',
				  'I': 'helix',
				  'G': 'helix',
				  'P': 'helix',
				  'B': 'strand',
				  'E': 'strand',
				  'T': 'other',
				  'S': 'other'}
				  
	structure_colors = {'helix': 'green',
						'strand':'blue',
						'other': 'white'}
						
	fig = go.Figure()
	
	res_width = 1
	res_height = 10
	index = 1
	x_centers = []
	y_centers = []
	hover_texts = []
	
	for row in chain_data:
		res_index = row['residue_index']
		ss = row['SS']
		structure = structures.get(ss, 'other')
		structure_color = structure_colors[structure]
		
		x_center = index + res_width / 2
		y_center = res_height / 2
		x_centers.append(x_center)
		y_centers.append(y_center)
		print(f"x_center:' {x_center}, y_center: {y_center}")
		hover_text = (f"DSSP index: {row['dssp_index']}<br>"
					  f"Residue index: {row['residue_index']}<br>"
					  f"Insertion code: {row['insertion_code']}<br>"
					  f"Chain ID: {row['chain_id']}<br>"
					  f"AA: {row['AA']}<br>"
					  f"SS: {row['SS']}")
		hover_texts.append(hover_text)
		
		
		
		fig.add_shape(type='rect',
					  x0=index, y0=0,
					  x1=index + res_width, y1=res_height,
					  fillcolor=structure_color,
					  line=dict(color="black"),
					  layer="below")
        			 
		index +=1
		
	fig.add_trace(go.Scatter(x=x_centers,
							 y=y_centers,
							 mode='markers',
							 marker=dict(color='rgba(0,0,0,0)',
							 			 size=res_width),
							 hoverinfo='text',
							 text=hover_texts))
	
	
	fig.update_layout(title="SS protein structure",
					  xaxis_title="Res index",
					  yaxis_visible=False,
					  height = res_height * 20,
					  xaxis=dict(range=[1, index + 1]))

	fig.show()
	 
			
