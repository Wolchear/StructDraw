# Plans:
The next thing I plan to do is clean up unnecessary code. At the very least,
the visualisation module still contains remnants of old ideas, redundant fields,
and other unused elements. Ideally, these should be removed before continuing
further development.
Additionally, I need to implement text rendering in DrawArea, including residue names,
indices, and other relevant information. It might also be worth allowing the user to
customize the size of Shapes.
Another important feature is implementing a "split" function for chains,
which users can control. Right now, chains are drawn as long, continuous
sequences in a single line, which makes interpretation difficult.
Allowing users to define custom splits would improve readability.
Once these tasks are complete, I will finalize the Title component and move o
to implementing a color palette system, so users can control how residues are colored.
Only after this will I complete the Legend, since it doesn’t make much sense without
a proper palette system in place.
## Long-Term Improvements
Finally, I’d like to explore adding support for alternative algorithms beyond DSSP.
To do this, I’ll likely need to create an abstract class (e.g., App) that would serve
as a base for both DSSP and any future algorithms (STRIDE, PROMOTIF etc.). I think this
is a good idea because we already allow adding individual chains to the drawing.
Extending this to let users compare the same chains processed by different algorithms
would add another valuable feature to the program.
# Modules info:
## Module 'structures':
### pdb_model:
This is the main base class that should be accessible to the user. Essentially,
it will be used for reading PDB files and storing the necessary information for
visualization: an array of chains, the file path, the file type, and possibly
something else. For now, I don’t have any grand plans.
### _chain
This should be a private class that stores information about the chains in the
pdb model: indices, residues, secondary structure, etc.
## Module 'dssp':
### dssp:
Essentially, it just runs the DSSP program and processes the output for further handling.
## Module 'visualization':
### visualization:
Currently, the file contains only a small number of functions that conveniently generate
images of a specific chain or the entire file
### Canvas:
A new class has been added in the current commit. It is responsible for generating the image.
In the program's code, an 'image' consists of three elements: Title, DrawArea, and Legend.
Why was this approach taken? In my opinion, creating an image as a single, monolithic entity
is much more complex than generating it from separate components. This approach also allows for
the dynamic addition and/or removal of objects even after the image has been generated and/or saved.
So far, out of the three elements, only the core part—DrawArea—has been implemented.
Therefore, I will now focus on discussing it in more detail.
#### DrawArea:
DrawArea is also not a monolithic object. Essentially, it serves as a dynamic storage for chains.
This means we can easily add and, in theory, remove sequences before generating the image.
DrawArea stores objects of the Chain class from the visualisation module
#### Chain:
Objects of the Chain class also serve only as storage for objects of the Shapes class.
Essentially, this results in the following data structure: a list of objects inside an object inside a list of objects.

Why was this approach taken?
I chose this structure to allow the use of relative coordinates for Shapes within a Chain,
while also avoiding the need to immediately assign fixed coordinates to Chains within DrawArea.

What are the advantages of this approach?
As I mentioned earlier, we don’t need to manually calculate and assign coordinates for each chain,
nor do we need to determine the exact size of DrawArea beforehand—the program takes care of all
calculations and displays everything correctly. This effectively turns the system into a sort of constructor.

Additionally, since coordinates are not hardcoded, we could, in theory, implement filters for sequence display,
such as sorting by increasing or decreasing length. Another major benefit is extensibility. It becomes significantly
easier to add new types of objects or Shapes. The existing functionality already works, and any
modifications will require only minor adjustments rather than a complete rewrite of the system.
### How to use
```
pip install -e .
./demo_run.py -pdb {pdb_file}`
```
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
