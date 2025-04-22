# User Guide

In this file, I’ll describe specific aspects of how to use the package.  
I hope this guide will help you better understand its capabilities and make your experience smoother.

## Table of Contents

- [File Import](#file-import)
  - [Stage 1: Model Initialization](#stage-1:-model-initialization)
  - [Stage 2: Chain Extraction](#stage-2:-chain-extraction)
- [Vsiualization](#vsiualization)
  - [Stage 1: Canvas initialization](#stage-1:-canvas-initialization)
  - [Stage 2: Adding a Chain to the Plot](#stage-2:-Adding-a-chain-to-the-plot)
  - [Stage 3: Chain Visualization Configuration](#stage-3:-chain-visualization-configuration)
  - [Stage Optional: Title](#stage-optional:-title)
  - [Stage 4: Rendering](#stage-4:-rendering)
- [Coloring Modes](#coloring-modes)
  - [Custom Palettes](#custom-palettes)
- [Coloring Modes](#coloring-modes)
  - [Custom Palettes](#custom-palettes)
- [Alignment Support](#alignment-support)
  - [Stage 1: Alignment Class Import](#stage-1:-alignment-class-import)
  - [Stage 2: Alignment Object Creation](#stage-2:-alignment-object-creation)
  - [Stage 3: Chain Extraction](#stage-3:-chain-extraction)

## File Import
### Stage 1: Model Initialization
To get started, we need to load a file for further processing.  
The first step is to create a **model** of our file. To do that, we must import the appropriate model class into our script.

There are two types of models available:
- `PDB` — for canonical `.pdb` files
- `PDBx` — for `.cif` files

Make sure to use the correct file format for the model you are creating.
```python
from struct_draw.structures.pdb_model import PDB, PDBx
```
The next step is to **create a model**.
To do this, you must provide two required parameters:
1. The **path to the PDB or PDBx file**
2. The **name of the algorithm** to use for secondary structure analysis

As of April 22, 2025, the following algorithms are supported:

- **DSSP**

- **Stride**

```python
pdb_model = PDB(algorithm_name='mkdssp', pdb_file=pdb_file)
```



> 📌 Note
>
> It's important to note that this is not the only way to create a model.  
> Instead of providing a PDB file, you can directly pass in the **output of the algorithm** (e.g., a precomputed DSSP or Stride file).
>
> ```python
> with open('dssp_out', 'r') as f:
>     dssp_content = f.read()
> pdb_model = PDB(algorithm_name='mkdssp', algorithm_out=dssp_content)
> ```
>
> However, keep in mind the following limitations:
>
> - The **algorithm name** must still match the format of the provided file.  
>   For example, you **cannot** load a Stride output while specifying `DSSP` or `MKDSSP` as the algorithm — this will not work.
> - This approach **disables coloring by B-factor**, since the original structural file is missing.  
>   If you want to use B-factor-based coloring, you must also provide the original PDB file along with the algorithm output.
> - You must provide the **already loaded content**, not just the path to the output file.  
>   That means you need to open and parse the file yourself before passing it into the model.


### Stage 2: Chain Extraction
After creating the model, don’t forget to extract the specific chain you need using its **chain ID** from the PDB file.  
We'll need this chain later for visualization.

```python
chain_A = pdb_model.get_chain('A')
```

## Vsiualization
### Stage 1: Canvas initialization

Once we've loaded our chains, it's time to visualize them.

Everything starts with importing the `Canvas` and `Chain` classes.  
We then create an instance of the `Canvas` — this is where everything will be "drawn."

To create a `Canvas` object, you only need to provide a single parameter: the **background color**.  
That's all the configuration it requires

```python
from struct_draw.plotter import Chain, Canvas
canvas = Canvas('white')
```

### Stage 2: Adding a Chain to the Plot

The next step is to add our chain to the plot.  
This process happens in two main stages:

1. **Create an instance of the `Chain` class** for visualization.  
   This object will contain all the graphical information related to the chain.

2. **Add the `Chain` to the `Canvas`** using the appropriate method.  
   This will place the visual representation of the chain onto the plot.
   
   
```python
new_chain = Chain(chain_A, shape_size=50, split=80, color_mode='b_factor', color_sub_mode='mean')
canvas.add_chain(new_chain)
```

### Stage 3: Chain Visualization Configuration

This is one of the most important steps: it’s where you configure how the chain will be displayed. Below is a breakdown of each parameter:

- **shape_size** `int`  
  Controls the drawing area for each Shape. It’s essentially the side length of the square container in which each shape (helix, strand, etc.) is rendered.

- **show_amino_code** `bool`  
  Whether to display the amino acid code label for each Shape.  
  **Default:** `True`  
  Set to `False` to hide all amino acid labels.

- **split** `int`  
  Determines how many Shapes appear per row. For example, if `split = 60`, the 61st residue will wrap to the next line below the first.  
  Useful for very long chains to prevent the plot from becoming excessively wide.

- **start** `int` & **end** `int`  
  Indexes for slicing the residue list: `residues[start:end]`.  
  - To display residues 1–80, use `start = 0, end = 80`.  
  - You don’t have to set both: to limit to the first 100 residues, just set `end = 100`; to start at residue 20, set `start = 20`.

- **chain_annotation** `Dict[str, bool]`  
  Specifies which chain metadata to display as labels. Available keys:  
  - `'chain_id'`  (Default: `True`)
  - `'algorithm'` (Default: `False`)
  - `'model_id'`  (Default: `True`)
  To hide all annotations, pass an empty dictionary or set all values to `False`.

- **color_mode** `str`  
  Defines the primary coloring strategy (e.g., `"b_factor"`, `"structure_type"`, etc.).

- **color_sub_mode** `str`  
  A sub‑mode for finer control over coloring (for example, choosing a specific ramp or gradient within the main mode).

- **custom_palette** `Dict[str, str]`  
  A mapping from categories (or residue types) to color codes. If omitted, the package’s default palette is used.

> 🔍 More details on coloring options will be covered in a dedicated “Coloring” section.

### Stage Optional: Title

You can add a title to the Canvas at any time—before adding chains, after adding chains, or even between them.  
The only requirement is that you set it **after** creating the `Canvas` instance and **before** rendering the image.

- **text_position** `str`  
  Specifies the alignment of the title. Possible values:  
  - `'left'` — align text to the left  
  - `'centered'` — center the text  
  - `'right'` — align text to the right  

  All options position the title according to their name.

```python
canvas.add_title(font='DejaVuSans.ttf',
                 font_size=50,
                 text='Test Title',
                 text_position='centered')
```
 
### Stage 4: Rendering
After you’ve added all the desired elements to the `Canvas`, you can render the final visualization very easily:

```python
image = canvas.get_image()
```

This call returns an image object (for example, a PIL Image).
From here, you’re free to do whatever you wish with it:
- Display it immediately in a notebook or GUI:
```python 
image.show()
```

- Save it to disk with:
```python 
image.save("output.png")
```

- Do anything else you want with it

Your image—your rules! 🎨


## Coloring Modes

As of April 22, 2025, three coloring modes are implemented. You must specify one of these names in the **color_mode** `str` parameter:

- **structure**  
- **aa** (amino acids)  
- **b_factor**  

Each mode also has its own sub‑modes (**color_sub_mode** `str`):

- **structure**  
  - `secondary` — colors individual secondary‑structure elements.

- **aa**  
  - `hydrophilicity` — colors residues based on hydrophilic vs. hydrophobic properties.  
  - `single_aa` — colors each amino acid individually.

- **b_factor**  
  - `mean` — computes the **mean** of the B‑factor vector for each residue and selects a color accordingly.  
  - `median` — computes the **median** of the B‑factor vector.  
  - `lowest` — uses the **minimum** B‑factor value.  
  - `highest` — uses the **maximum** B‑factor value.  
  - `a_fold` — computes the mean B‑factor but applies the AlphaFold palette (see [ChimeraX palettes](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/palettes.html)).

### Custom Palettes

Each coloring **mode** and **sub_mode** comes with at least one default palette, but you can provide your own custom palette. Keep in mind that each sub_mode expects a specific palette structure:

- **structure / secondary**  
  Provide a mapping from secondary‐structure class names to color codes.  
  Example default palette:
```python
DEFAULT_STRUCTURES_COLORS = {'helix': 'green',
                             'strand': 'blue',
                             'other': 'white',
                             'gap': 'black'}
```
- **b_factor**  
Provide a mapping from (min, max) B‑factor ranges to color codes.
Example default palette:
```python
DEFAULT_PALETTE = {(0,   20):  '#0000FF',  # blue
                   (20,  40):  '#00FFFF',  # cyan
                   (40,  60):  '#00FF00',  # green
                   (60,  80):  '#FFFF00',  # yellow
                   (80, 200):  '#FF0000'}  # red
```

## Alignment Support

`struct_draw` also supports rendering entire alignments. The workflow is very similar to adding individual chains, with a few extra steps.

### Stage 1: Alignment Class Import

```python
   from struct_draw.structures.alignment import Alignment
```

### Stage 2: Alignment Object Creation
You need to provide three parameters in this order:
- **alignment_file** `str`: the path of your FASTA‑formatted alignment
- **pdb_files_dir**  `str`: directory where your PDB/PDBx files are stored
- **algorithm_name** `str`: the secondary‑structure algorithm to use (e.g., "mkdssp")

```python
new_alignment = Alignment(alignment, pdb_files_dir, 'mkdssp')
```

### Stage 3: Chain Extraction
Once the Alignment object is created, you can iterate over its models and chains just like before.
```python
for model in new_alignment.models:
    for chain in model.get_chain_list():
        chain_to_add = model.get_chain(chain)
        canvas.add_chain(Chain(chain_to_add,
                               shape_size=50,
                               split=80,
                               color_mode='structure',
                               color_sub_mode='secondary'))
```

