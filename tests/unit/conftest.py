from typing import Dict, Optional
import importlib

import pytest

from struct_draw.apps.algorithms import DSSP

@pytest.fixture(scope="session")
def make_dssp():
    """Fixture for dssp algorithms obj factory"""
    def _make_dssp(algorithm_sub_name: str, ss_translation: Optional[Dict[str,str]]):
        return DSSP(algorithm_sub_name, ss_translation)
    
    return _make_dssp

@pytest.fixture(scope='session')
def ss_custom() -> Dict[str, str]:
    return {'H': 'Other',
            'G': 'Other',
            'I': 'Other',
            'E': 'Other',
            'B': 'Other',
            'T': 'Other',
            'S': 'Other'}
    
@pytest.fixture(scope='session')
def default_table() -> Dict[str, str]:
    return {'H': 'Helix',
            'G': 'Helix',
            'I': 'Helix',
            'E': 'Strand',
            'B': 'Strand',
            'T': 'Other',
            'S': 'Other'}

@pytest.fixture(scope="session")
def dssp_module():
    return importlib.import_module(DSSP.__module__)

@pytest.fixture(scope="session")
def make_line():
    def _make_line(res_idx, ins=" ", chain="A", aa="G", ss_code="H", make_space_for_dash=False):
        buf = [" "] * 80
        s = f"{res_idx:5d}"
        buf[5:10] = list(s)
        buf[10] = ins
        buf[11] = chain
        buf[13] = aa
        if make_space_for_dash:
            pass
        else:
            buf[16] = ss_code 
        return "".join(buf)
    
    return _make_line