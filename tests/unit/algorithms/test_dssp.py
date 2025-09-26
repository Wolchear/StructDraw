import subprocess

import pytest

class TestDSSP:
    ALGO = ["dssp", "mkdssp"]
    TABLE = ["default", "custom"]
    
    @pytest.mark.parametrize("algo_name", ALGO, ids=ALGO)
    @pytest.mark.parametrize("table_kind", TABLE, ids=TABLE)
    def test_translation(self, make_dssp, ss_custom, algo_name, default_table, table_kind):
        table = None if table_kind == "default" else ss_custom
        dssp = make_dssp(algo_name, table)
        ref_table = default_table if table_kind == "default" else ss_custom
        assert dssp.SS_TRANSLATION == ref_table
        
        
    def test_run_with_monkeypatch(self, make_dssp, tmp_path, dssp_module, monkeypatch):

        pdb_path = tmp_path / "dummy3.pdb"
        pdb_path.write_text("ATOM ...\n")

        dssp = make_dssp("dssp", None)
        class _DummyProc:
            def __init__(self, *args, **kwargs):
                        self.args = args
                        self.kwargs = kwargs
            def communicate(self):
                        return ("MOCK_DSSP_OUTPUT", "")

        def _fake_popen(cmd, **kwargs):
            assert cmd[:2] == ["dssp", "--output-format=dssp"]
            assert cmd[2] == str(pdb_path)
            assert kwargs["stdout"] is subprocess.PIPE
            assert kwargs["stderr"] is subprocess.PIPE
            assert kwargs["universal_newlines"] is True
            return _DummyProc()
        
        monkeypatch.setattr(dssp_module.subprocess, "Popen", _fake_popen, raising=True)

        out = dssp.run(str(pdb_path))
        assert out == "MOCK_DSSP_OUTPUT"
        
    class TestProcess():
        @pytest.mark.parametrize(
             "lines, header, expected_len",
             [
                 pytest.param(
                     [(1, " ", "A", "A", "H"),
                     (2, " ", "A", "V", "E"),
                     (3, " ", "B", "G", "H", True)],
                     "XXX RESIDUE AA STRUCTURE XXX\n",
                     3,
                      id='good_data+good_header',
                 ),
                 pytest.param(
                     [(1, " ", "A", "A", "H"),
                     (2, " ", "A", "V", "E"),
                     (3, " ", "B", "G", "H", True)],
                     "garbage header\n",
                     0,
                     id='good_data+bad_header',
                 ),
                 pytest.param(
                     [],
                     "XXX RESIDUE AA STRUCTURE XXX\n",
                     0,
                     id='bad_data+bad_header',
                 )
             ]
            
        )
        def test_process_data_basic(self, make_dssp, make_line, lines, header, expected_len):
            dssp = make_dssp("dssp", None)
            body = "\n".join(make_line(*args) for args in lines)
            algorithm_out = header + body + "\n"
            arr = dssp.process_data(algorithm_out)
            assert len(arr) == expected_len
            assert arr.dtype.names == ("residue_index", "insertion_code", "chain_id", "AA", "SS", "SS_code")
            if expected_len:
                assert arr["residue_index"][0] == lines[0][0]
                assert arr["chain_id"][0] == lines[0][2]
                assert arr["AA"][0] == lines[0][3]
                codes = arr["SS_code"].tolist()
                if any(t[-1] is True for t in lines):
                    assert "-" in codes
                    idx = codes.index("-")
                    assert arr["SS"][idx] == "Other"
                    
        def test_process_custom_dict(self, make_dssp, make_line, ss_custom):
            dssp = make_dssp("dssp", ss_custom)
            header = "XXX RESIDUE AA STRUCTURE XXX\n"
            line = make_line(1, " ", "A", "A", "H")  # SS_code=H
            # by default H should be translated as 'Helix', but with custom it has to be 'Other'
            
            arr = dssp.process_data(header + line + "\n")
            assert len(arr) == 1
            assert arr["SS_code"][0] == "H"
            assert arr["SS"][0] == "Other"
            
        def test_process_data_unknown_code_falls_back_to_other(self, make_dssp, make_line):
            dssp = make_dssp("dssp", None)  # default table
            header = "XXX RESIDUE AA STRUCTURE XXX\n"
            line = make_line(2, " ", "A", "G", "X")  # There is no 'X' in deault table
            arr = dssp.process_data(header + line + "\n")
            assert arr["SS_code"][0] == "X"
            assert arr["SS"][0] == "Other"
            
        def test_custom_translation_not_mutated(self, make_dssp):
            """A function that should check whether the table is mutated during the function's execution."""
            mapping = {'H': 'Helix',
                        'G': 'Helix',
                        'I': 'Helix',
                        'E': 'Strand',
                        'B': 'Strand',
                        'T': 'Other',
                        'S': 'Other'} # default table
            dssp = make_dssp("dssp", mapping)
            _ = dssp.SS_TRANSLATION['H'] 
            assert mapping['H'] == 'Helix'