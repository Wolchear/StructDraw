# Struct Draw

**Struct Draw** is a Python package for generating plots and visualizations of protein secondary structure based on the output of algorithms such as DSSP and Stride.

## Table of Contents

- [Description](#description)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)   
- [License](#license)
- [Dependencies](#dependencies)  

## Description

**Struct Draw** makes it easy to visualize protein secondary structure elements α‑helices, β‑sheets, turns, etc.—by parsing the output of common annotation tools (DSSP, Stride) and rendering figures.

## Features

- **PDB/PDBx support** — parse and visualize raw PDB or PDBx/mmCIF files.  
- **DSSP & Stride compatibility** — read canonical DSSP and Stride output (with optional limited coloring).  
- **2D secondary‑structure plots** — display helices, sheets, and other elements in PNG.  
- **Palette flexibility** — choose from built‑in color schemes or supply your own custom palettes.  
- **Intuitive API** — a simple, Pythonic interface for building and customizing plots.  
- **Extensible architecture** — plug in your own parsing algorithms or coloring modes seamlessly.
- **Alignment support** — visualize and compare sequence or structural alignments alongside secondary‑structure plots.  

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/StructDraw.git
cd StructDraw
pip install -e .
```

## Usage
### PDB files
```python
#!/usr/bin/env python3

from struct_draw.structures.pdb_model import PDB, PDBx
from struct_draw.plotter import Chain, Canvas

data_dir = 'data/'

pdb_file = data_dir + '1ad0.pdb'
predicted_pdb_file = data_dir + '1ad0_predicted.cif'

canvas = Canvas('white')
canvas.add_title('DejaVuSans.ttf', 50, 'True and Predicted Chains Comparison', 'centered')

pdb_model = PDB('mkdssp', pdb_file)
chain_A = pdb_model.get_chain('A')
canvas.add_chain(Chain(chain_A,
                       shape_size=50,
                       split=80,
                       color_mode='b_factor',
                       color_sub_mode='mean'))

predicted_model = PDBx('mkdssp', predicted_pdb_file)
predicted_chain_A = predicted_model.get_chain('A')
canvas.add_chain(Chain(predicted_chain_A,
                       shape_size=50,
                       split=80,
                       color_mode='b_factor',
                       color_sub_mode='a_fold'))

img = canvas.get_image()
img.save('output_image.png')
img.show()
```
![Usage Script Reult](https://github.com/Wolchear/StructDraw/main/usage_example/output_image.png)

### Alignment

```python
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
        canvas.add_chain(Chain(chain_to_add,
                               shape_size=50,
                               split=80,
                               color_mode='structure',
                               color_sub_mode='secondary',
                               custom_palette=NEW_PALETTE))
    
img = canvas.get_image()
img.save('alignment_output_image.png')
img.show()
```
![Alignment Usage Script Reult](https://github.com/Wolchear/StructDraw/main/usage_example/alignment_output_image.png)

## Dependencies

- Python ≥ 3.10  
- numpy ≥ 1.26.1,<2.0  
- Pillow ≥ 11.1.0,<12.0  

> **Note:** Struct Draw was developed and tested on the versions listed above.  
> It has not been tested on earlier versions, so compatibility with lower versions is not guaranteed.

## License

This project is licensed under the [BSD‑3‑Clause License](https://opensource.org/licenses/BSD-3-Clause).

