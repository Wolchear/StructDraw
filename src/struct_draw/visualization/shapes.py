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
