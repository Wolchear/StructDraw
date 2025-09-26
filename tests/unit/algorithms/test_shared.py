import subprocess
import importlib

import pytest

from struct_draw.apps.algorithms import DSSP, Stride

@pytest.fixture(scope='session')
def make_module():
    """Module factory"""
    def _make(cls):
        return importlib.import_module(cls.__module__)
    return _make

class TestShared():
    @pytest.mark.parametrize(
        "algo_params, algo_name",
        [
            pytest.param((DSSP, 'dssp'), 'dssp', id='dssp+dssp'),
            pytest.param((DSSP, 'mkdssp'), 'dssp', id='dssp+mkdss'),
            pytest.param((Stride, 'stride'), 'stride', id='stride'),
        ]
    )
    def test_translation_shared(self, make_algorithm, algo_params, algo_name,
                                default_table_dssp, default_table_stride, ss_custom):
        cls, subcmd = algo_params
        algo = make_algorithm(cls, subcmd, None)
        expected_default = default_table_dssp if algo_name == "dssp" else default_table_stride
        assert algo.SS_TRANSLATION == expected_default

        algo = make_algorithm(cls, subcmd, ss_custom)
        assert algo.SS_TRANSLATION == ss_custom
    
    @pytest.mark.parametrize(
        "algo_params, communicate_out",
        [
            pytest.param((DSSP, 'dssp'), "MOCK_DSSP_OUTPUT", id='dssp+dssp'),
            pytest.param((DSSP, 'mkdssp'), "MOCK_MKDSSP_OUTPUT", id='dssp+mkdss'),
            pytest.param((Stride, 'stride'), "MOCK_STRIDE_OUTPUT", id='stride'),
        ]
    )
    def test_run_with_monkeypatch(self, make_algorithm, make_module, tmp_path,
                                  monkeypatch, algo_params, communicate_out):

        pdb_path = tmp_path / "dummy3.pdb"
        pdb_path.write_text("ATOM ...\n")
        cls, subcmd = algo_params
        algo = make_algorithm(cls, subcmd, None)
        class _DummyProc:
            def __init__(self, *args, **kwargs):
                        self.args = args
                        self.kwargs = kwargs
            def communicate(self):
                        return (communicate_out, "")

        if cls is DSSP:
            expected_cmd = [subcmd, "--output-format=dssp", str(pdb_path)]
        elif cls is Stride:
            expected_cmd = [subcmd, str(pdb_path)] 
        else:
            raise AssertionError("Unknown algorithm class")
        
        def _fake_popen(cmd, **kwargs):
            assert cmd == expected_cmd
            assert kwargs["stdout"] is subprocess.PIPE
            assert kwargs["stderr"] is subprocess.PIPE
            assert kwargs["universal_newlines"] is True
            return _DummyProc()
        
        module = make_module(cls)
        monkeypatch.setattr(module.subprocess, "Popen", _fake_popen, raising=True)

        out = algo.run(str(pdb_path))
        assert out == communicate_out