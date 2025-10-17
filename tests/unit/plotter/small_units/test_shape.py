from dataclasses import dataclass

import pytest
import numpy as np

from struct_draw.plotter.small_units.shape import BaseShape, Other, Helix, Strand, Gap



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
        

    @pytest.mark.parametrize(
        "cls,pos,size,base_pts",
        [
            # ---------- Other ----------
            (
                Other,
                "any",
                100,
                [(0.0, 0.3), (1.0, 0.7)],
            ),
            # ---------- Helix ----------
            (
                Helix,
                "first",
                100,
                [
                    (0.0, 0.3), (0.4, 0.3), (0.6, 0.1), (1.0, 0.1),
                    (1.0, 0.5), (0.8, 0.5), (0.6, 0.7), (0.0, 0.7),
                ],
            ),
            (
                Helix,
                "inner",
                80,
                [
                    (0.0, 0.1), (0.2, 0.1), (0.4, 0.25), (0.6, 0.25),
                    (0.8, 0.1), (1.0, 0.1), (1.0, 0.5), (0.8, 0.5),
                    (0.7, 0.7), (0.3, 0.7), (0.2, 0.5), (0.0, 0.5),
                ],
            ),
            (
                Helix,
                "last",
                50,
                [
                    (0.0, 0.1), (0.5, 0.1), (0.7, 0.3), (1.0, 0.3),
                    (1.0, 0.7), (0.4, 0.7), (0.2, 0.5), (0.0, 0.5),
                ],
            ),
            # ---------- Strand ----------
            (
                Strand,
                "first",
                120,
                [(0.0, 0.2), (1.0, 0.8)],
            ),
            (
                Strand,
                "inner",
                64,
                [(0.0, 0.2), (1.0, 0.8)],
            ),
            (
                Strand,
                "last",
                90,
                [
                    (0.0, 0.2), (0.4, 0.2), (0.4, 0.0),
                    (1.0, 0.5), (0.4, 1.0), (0.4, 0.8), (0.0, 0.8),
                ],
            ),
            # ---------- Gap ----------
            (
                Gap,
                "any",
                100,
                [(0.1, 0.5), (0.9, 0.5)],
            ),
        ],
    )
    def test_get_points_coficients_unified(self, cls, pos, size, base_pts):
        res = cls._get_points_coficients(pos, size )
        
        expected = np.array(base_pts, dtype=np.float32) * size
        expected = np.rint(expected).astype(np.int32)
        assert res.dtype == np.int32

        np.testing.assert_array_equal(res, expected)


    @pytest.mark.parametrize("cls", [Helix, Strand])
    def test_get_points_coficients_invalid_pos_raises(self,cls):
        with pytest.raises(ValueError):
            cls._get_points_coficients("unknown", 100)