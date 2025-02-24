import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Chain:
    def __init__(self, chain_data: np.ndarray, color_structures: str):
        self.__chain_data = chain_data
        self.__residues_quantity = len(chain_data)
        self.__color_structures = color_structures
        self.__shape_size = 10
        self.__width = self.__residues_quantity * self.__shape_size + 2 * self.__shape_size
        self.__heigth = 2 * self.__shape_size
        self.__shapes_storage = self._generate_shapes()
    
    def _generate_shapes(self):
        shape_storage = np.empty(self.__residues_quantity, dtype=object)
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
                            
        for index, row in enumerate(self.__chain_data):
            ss = row['SS']
            aa = row['AA']
            residue_index = row['residue_index']
            insertion_code = row['insertion_code']
            structure = structures.get(ss, 'other')
            fillcolor = structure_colors[structure]
            font = ImageFont.load_default()
            x0 = index * self.__shape_size + self.__shape_size * 0.5
            y0 = self.__shape_size * 0.5
            shape_storage[index] = Shape(10, 10, residue_index, insertion_code,
                                                 fillcolor, aa, ss, x0, y0, font, 14)
         
        return shape_storage
                                                 
    def get_shapes(self):
        return self.__shapes_storage
        
    def get_width(self):
        return self.__width
        
    def get_heigth(self):
        return self.__heigth
    
class Shape():
    def __init__(self, width: int, heigth: int, residue_index: int, insertion_code:str, color: str,
                 amino_acid: str, secondary_structure:str, x_0:int, y_0:int, font: str, font_size: int):
        self.width = width
        self.heigth = heigth
        self.residue_index = residue_index
        self.insertion_code = insertion_code
        self.color = color
        self.amino_acid = amino_acid
        self.secondary_structure = secondary_structure
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = self.x_0 + self.width
        self.y_1 = self.y_0 + self.heigth
        self.font = font
        self.font_size = font_size
		
    def get_shape_params(self):
        shape_tuple = ([self.x_0, self.y_0, self.x_1, self.y_1],
                       self.color, 'black')
        font_tuple = (self.font_size, self.font)
        info_tuple = (self.residue_index, self.insertion_code,
                      self.amino_acid, self.secondary_structure)
        return shape_tuple, font_tuple, info_tuple
