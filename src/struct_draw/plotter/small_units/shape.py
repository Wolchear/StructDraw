from dataclasses import dataclass, field
from typing import Dict, Optional
from abc import ABC, abstractmethod
from math import ceil

from PIL import Image, ImageDraw, ImageFont, ImageColor
from .label import RegularLabel

@dataclass
class BaseShape(ABC):
    """
    Abstract base class for drawable shapes representing residues.

    Attributes:
        _residue (object): Object containing residue information, including amino_acid.
        _size (int): Size of the shape in pixels.
        _color (str): Fill color of the shape (hex string or color name).
        _show_amino_code (bool): Flag to display the one-letter amino acid code.
        _pos_in_structure (str): Position identifier within a larger structure.
        _amino_label (RegularLabel): Label object for amino acid code (initialized if needed).
        _font_size (int): Font size for the amino acid label (calculated automatically).
        _font (str): Path to the font file used for label rendering.
        _font_color (str): Color of the font for the amino label (calculated for contrast).
    """
    _residue: object
    _size: int
    _color: str
    _show_amino_code: bool
    _pos_in_structure: str
    _amino_label: RegularLabel = field(init=False, default=None)
    _font_size: int = field(init=False, default=None)
    _font: str = field(default='DejaVuSans.ttf')
    _font_color: str = field(init=False, default=None)

    @property
    def height(self):   
        return self._size
    
    def __post_init__(self) -> None:
        """
        Post-initialization to prepare the amino acid label if requested:
        - Calculates a contrasting font color against the shape's fill color.
        - Determines font size as a fraction of the shape size.
        - Generates the RegularLabel for the amino acid code.
        """
        if self._show_amino_code:
            self._font_color = self.get_contrast_color(self._color)
            self._font_size =  self._size * 0.4
            self._amino_label = self._generate_amino_annotation()
    
    
    def get_contrast_color(self, bg_color: str, threshold: int = 128) -> str:
        """
        Determines a contrasting font color based on background brightness.

        Args:
            bg_color (str): Background color as '#RRGGBB' or standard color name.
            threshold (int): Luminance threshold (0-255) to switch contrast.

        Returns:
            str: '#FFFF99' if background is dark, '#000000' if light.
        """
        r, g, b = ImageColor.getrgb(bg_color)
        luminance = 0.299*r + 0.587*g + 0.114*b
        return '#FFFF99' if luminance < threshold else '#000000' 
     
    
    def _generate_amino_annotation(self) -> RegularLabel:
        return RegularLabel(self._residue.amino_acid, self._font_size, self._font, self._font_color)
    
    def draw(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        """
        Draws the shape and optionally centers the amino acid code label within it.

        Args:
            x_0 (int): X-coordinate of the top-left corner for drawing the shape.
            y_0 (int): Y-coordinate of the top-left corner for drawing the shape.
            draw_context (ImageDraw.ImageDraw): The PIL ImageDraw drawing context.
        """
        self._draw_self(x_0, y_0, draw_context) # Draw the spicific shape (Strand, Helix, Other or Gap)
        amino_label_x_0 = x_0 + int(self._size * 0.5)
        if self._show_amino_code:
            # Center the label inside the shape
            amino_label_x_0 = x_0 + (self._size - self._amino_label.width) // 2
            amino_label_y_0 = y_0 + (self._size - self._amino_label.height) // 2
            
            # Adjust for font offse
            adjusted_x = amino_label_x_0 - self._amino_label._offset_x
            adjusted_y = amino_label_y_0 - self._amino_label._offset_y
            
            self._amino_label.draw(adjusted_x, adjusted_y, draw_context)
    
        
    @abstractmethod
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        """
        Abstract method to draw the specific shape form onto the provided context.

        Args:
            x_0 (int): X-coordinate of the top-left corner for drawing.
            y_0 (int): Y-coordinate of the top-left corner for drawing.
            draw_context (ImageDraw.ImageDraw): The PIL ImageDraw drawing context.
        """
        pass

            
@dataclass        
class Other(BaseShape):    
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        fixed_y_0 = y_0 + int(self._size * 0.3)
        fixed_y_1 = y_0 + int(self._size * 0.7)
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.03)
        draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        
     
@dataclass
class Helix(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        points = []
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        outline_width = ceil(self._size * 0.05)
        if self._pos_in_structure == 'first':
            points = [ (x_0,                         y_0 + int(self._size * 0.3)), # A
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.3)), # B
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.1)), # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.1)), # D
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # E
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.5)), # F
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.7)), # G
                       (x_0,                         y_0 + int(self._size * 0.7))] # H
        elif self._pos_in_structure == 'inner':
            points = [ (x_0,                         y_0 + int(self._size * 0.1)), # A
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.1)), # B
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.25)),# C
                       (x_0 + int(self._size * 0.6), y_0 + int(self._size * 0.25)),# D
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.1)), # E
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.1)), # F
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # G
                       (x_0 + int(self._size * 0.8), y_0 + int(self._size * 0.5)), # H
                       (x_0 + int(self._size * 0.7), y_0 + int(self._size * 0.7)), # K
                       (x_0 + int(self._size * 0.3), y_0 + int(self._size * 0.7)), # L
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.5)), # M
                       (x_0,                         y_0 + int(self._size * 0.5))] # N
        elif self._pos_in_structure == 'last':
            points = [ (x_0,                         y_0 + int(self._size * 0.1)), # A
                       (x_0 + int(self._size * 0.5), y_0 + int(self._size * 0.1)), # B
                       (x_0 + int(self._size * 0.7), y_0 + int(self._size * 0.3)), # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.3)), # D
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.7)), # E
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.7)), # F
                       (x_0 + int(self._size * 0.2), y_0 + int(self._size * 0.5)), # G
                       (x_0,                         y_0 + int(self._size * 0.5))] # H
                       
                  
        draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)

@dataclass
class Strand(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        outline_width = ceil(self._size * 0.05)
        if self._pos_in_structure == 'first' or self._pos_in_structure == 'inner':
            x_1 = x_0 + self._size
            fixed_y_0 = y_0 + int(self._size * 0.2)
            fixed_y_1 = y_0 + int(self._size * 0.8)
            draw_context.rectangle([x_0, fixed_y_0 , x_1, fixed_y_1],
                                fill=self._color, outline='black', width=outline_width)
        else:
            points = [ (x_0,                         y_0 + int(self._size * 0.2)), # A
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.2)), # B
                       (x_0 + int(self._size * 0.4), y_0),                         # C
                       (x_0 + int(self._size),       y_0 + int(self._size * 0.5)), # D
                       (x_0 + int(self._size * 0.4), y_0 + self._size),            # E
                       (x_0 + int(self._size * 0.4), y_0 + int(self._size * 0.8)), # F
                       (x_0,                         y_0 + int(self._size * 0.8))] # G
            draw_context.polygon(points, outline="black", fill=self._color, width=outline_width)
        
        
@dataclass
class Gap(BaseShape):
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        x_1 = x_0 + self._size
        y_1 = y_0 + self._size
        y_0 = y_0 + 0.5 * self._size
        margin = self._size * 0.1
        width = ceil(self._size * 0.05)
        draw_context.line([x_0 + margin, y_0, x_1 - margin, y_0],
                                   		fill='black')
