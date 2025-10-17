from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from math import ceil
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np

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
    @staticmethod
    def _get_points_coficients(pos: str, size: int) -> np.ndarray:
        return np.rint(np.array([
            (0.0, 0.3),
            (1.0, 0.7)
        ], dtype=np.float32) * size ).astype(np.int32)
        
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        points = self._get_points_coficients(self._pos_in_structure, self._size)
        points[:, 0] += x_0        
        points[:, 1] += y_0
        outline_width = ceil(self._size * 0.03)
        draw_context.rectangle([tuple(p) for p in points.tolist()],
                                fill=self._color, outline='black', width=outline_width)
        
     
@dataclass
class Helix(BaseShape):
    @staticmethod
    def _get_points_coficients(pos: str, size: int) -> np.ndarray:
        if pos == 'first':
            pts = [
                (0.0, 0.3), # A
                (0.4, 0.3), # B
                (0.6, 0.1), # C
                (1.0, 0.1), # D
                (1.0, 0.5), # E
                (0.8, 0.5), # F
                (0.6, 0.7), # G
                (0.0, 0.7), # H
            ]
        elif pos == 'inner':
            pts = [
                (0.0, 0.1),  # A
                (0.2, 0.1),  # B
                (0.4, 0.25), # C
                (0.6, 0.25), # D
                (0.8, 0.1),  # E
                (1.0, 0.1),  # F
                (1.0, 0.5),  # G
                (0.8, 0.5),  # H
                (0.7, 0.7),  # K
                (0.3, 0.7),  # L
                (0.2, 0.5),  # M
                (0.0, 0.5),  # N
            ]
        elif pos == 'last':
            pts = [
                (0.0, 0.1), # A
                (0.5, 0.1), # B
                (0.7, 0.3), # C
                (1.0, 0.3), # D
                (1.0, 0.7), # E
                (0.4, 0.7), # F
                (0.2, 0.5), # G
                (0.0, 0.5), # H
            ]
        else:
            raise ValueError(f"Unknown pos: {pos}")
        float_points =  np.array(pts, dtype=np.float32) * size
        return np.rint(float_points).astype(np.int32)
        
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        points = self._get_points_coficients(self._pos_in_structure, self._size) 
        outline_width = ceil(self._size * 0.05)
        points[:, 0] += x_0        
        points[:, 1] += y_0
        draw_context.polygon([tuple(p) for p in points.tolist()], outline="black", fill=self._color, width=outline_width)

@dataclass
class Strand(BaseShape):
    @staticmethod
    def _get_points_coficients(pos: str, size: int) -> np.ndarray:
        if pos == 'first' or pos == 'inner':
            pts = [
                (0.0, 0.2),
                (1.0, 0.8)
            ]
        elif pos == 'last':
            pts = [
                (0.0, 0.2), # A
                (0.4, 0.2), # B
                (0.4, 0.0), # C
                (1.0, 0.5), # D
                (0.4, 1.0), # E
                (0.4, 0.8), # F
                (0.0, 0.8)  # G
            ]
        else:
            raise ValueError(f"Unknown pos: {pos}")    
        float_points =  np.array(pts, dtype=np.float32) * size
        return np.rint(float_points).astype(np.int32)
    
    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        outline_width = ceil(self._size * 0.05)
        points=self._get_points_coficients(self._pos_in_structure, self._size)
        points[:, 0] += x_0        
        points[:, 1] += y_0
        if self._pos_in_structure in ('first', 'inner'):
            draw_context.rectangle([tuple(p) for p in points.tolist()], fill=self._color, outline='black', width=outline_width)
        else:
            draw_context.polygon([tuple(p) for p in points.tolist()], outline="black", fill=self._color, width=outline_width)
        
        
@dataclass
class Gap(BaseShape):
    def _get_points_coficients(pos: str, size: int) -> np.ndarray:
        return  np.rint(np.array([
            (0.1, 0.5),
            (0.9, 0.5)
        ], dtype=np.float32) * size).astype(np.int32)

    def _draw_self(self, x_0: int, y_0: int, draw_context: 'ImageDraw.ImageDraw') -> None:
        points = self._get_points_coficients(self._pos_in_structure, self._size)
        points[:, 0] += x_0        
        points[:, 1] += y_0
        draw_context.line([tuple(p) for p in points.tolist()],
                                   		fill='black')
