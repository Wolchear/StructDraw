from typing import Optional, Dict

import pytest
import numpy as np

@pytest.fixture
def make_algorithm():
    """Algorithm factory"""
    def _make(cls, algorithm_sub_name: str, ss_translation: Optional[Dict[str, str]] = None):
        return cls(algorithm_sub_name, ss_translation)
    return _make

@pytest.fixture(scope='session')
def default_table_dssp() -> Dict[str, str]:
    return {'H': 'Helix',
            'G': 'Helix',
            'I': 'Helix',
            'E': 'Strand',
            'B': 'Strand',
            'T': 'Other',
            'S': 'Other'}
    
@pytest.fixture(scope='session')
def default_table_stride() -> Dict[str, str]:
    return  {'H': 'Helix',
             'G': 'Helix',
             'I': 'Helix',
             'E': 'Strand',
             'B': 'Strand',
             'T': 'Other',
             'C': 'Other'}

@pytest.fixture(scope='session')
def ss_custom() -> Dict[str, str]:
    return {'H': 'Other',
            'G': 'Other',
            'I': 'Other',
            'E': 'Other',
            'B': 'Other',
            'T': 'Other',
            'S': 'Other'}
    
    
class FakeAlgorithm:
    def __init__(self, rows):
        self._rows = rows

    def run(self, pdb_path):
        return "fake_out"

    def process_data(self, algorithm_out):
        return np.array(self._rows, dtype=object)

@pytest.fixture(scope='session')
def fake_algorithm_rows():
    return [
        dict(chain_id="A", residue_index=1, insertion_code=" ", AA="M", SS="Рelix", SS_code="H"),
        dict(chain_id="A", residue_index=2, insertion_code=" ", AA="E", SS="Рelix", SS_code="H"),
        dict(chain_id="B", residue_index=1, insertion_code=" ", AA="G", SS="Strand",  SS_code="B"),
    ]

@pytest.fixture(scope='session')
def patch_get_algorithm(monkeypatch, fake_algorithm_rows):
    def _patch(rows=None):
        rows = fake_algorithm_rows if rows is None else rows
        def _factory(name):
            return FakeAlgorithm(rows)
        from struct_draw.apps import interface
        monkeypatch.setattr(interface, "get_algorithm", _factory)
    return _patch