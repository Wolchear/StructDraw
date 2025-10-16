from dataclasses import dataclass

import pytest

from struct_draw.plotter.small_units.shape import BaseShape



class TestShape:
    class DummyShape(BaseShape):
        def _draw_self(self):
            pass
    
    @dataclass
    class FakeResidue:
        amino_acid: str = "A"
    
    @pytest.mark.parametrize(
        "bg_color, ref_color, threshold",
        [
            pytest.param(
                '#000000',
                '#FFFF99',
                128,
                id='black->yellow_lum_treshold_128',
            ),
            pytest.param(
                '#FFFF99',
                '#000000',
                128,
                id='yellow->black_lum_treshold_128',
            ),
            pytest.param(
                '#000000',
                '#000000',
                0,
                id='black->black_lum_treshold_0',
            )
        ]
    )
    def test_get_contrast_color(self, bg_color: str, threshold: int, ref_color: str):
        fake_resiudue = self.FakeResidue()
        dummy_shape = self.DummyShape(fake_resiudue, 10, bg_color , False, 'inner')
        font_color = dummy_shape.get_contrast_color(bg_color, threshold)
        assert font_color == ref_color
    
    @pytest.mark.parametrize(
        'generate_label, is_label',
        [
            pytest.param(
                True,
                True,
                id='annotation_exist',
            ),
            pytest.param(
                False,
                False,
                id='annotation_do_not_exist',
            )
        ]
    )
    def test_generate_amino_annotation(self, generate_label: bool, is_label: bool):
        fake_resiudue = self.FakeResidue()
        dummy_shape = self.DummyShape(fake_resiudue, 10, '#000000' , generate_label, 'inner')
        
        assert (dummy_shape._amino_label is not None) == is_label