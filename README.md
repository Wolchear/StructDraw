I finally, as it seems to me, understand how I would like to structure the package
# Plans:
## Module structures:
### pdb_model:
This is the main base class that should be accessible to the user. Essentially,
it will be used for reading PDB files and storing the necessary information for
visualization: an array of chains, the file path, the file type, and possibly
something else. For now, I don’t have any grand plans.
### _chain
This should be a private class that stores information about the chains in the
pdb model: indices, residues, secondary structure, etc.
## Module dssp:
### dssp:
I think using a class here is unjustified. In reality, this module should only
provide the ability to run DSSP within the package. Storing this information
should be handled by the previously described classes, as I see it.
## Module visualization:
### visualization:
Currently, the functions are focused on using and displaying only a single chain.
I am sure that once I finish the structural classes, it will not be difficult
for me to improve the current functions, as in their current form, they resemble
prototypes rather than a fully functional version.
### How to use
```
pip install -e .
./demo_run.py -pdb {pdb_file}`
```
This should generate an interactive graph and open it in the browser.
The graph is interactive, meaning that when hovering over a 'square,'
information about the residue will be displayed.

For now, everything is colored in the standard way, depending on the structure.
```
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
```
