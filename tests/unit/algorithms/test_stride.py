import pytest

from struct_draw.algorithms.algorithms import Stride


@pytest.fixture(scope="session")
def make_line():
    def _make_line(res_idx: int,
              ins: str = "",
              chain: str = "A",
              aa3: str = "GLY",
              ss_code: str = "H",
              ignore_asg = False):
        buf = [" "] * 80
        buf[0:3] = list("ASG") if not ignore_asg else ''
        aa3 = (aa3 or "GLY")[:3].ljust(3)
        buf[5:8] = list(aa3)
        buf[9] = (chain or "A")[0]
        if ins:
            resid_block = f"{res_idx:4d}{ins[0]}"
        else:
            resid_block = f"{res_idx:5d}"
        buf[10:15] = list(resid_block)
        buf[24] = (ss_code or "C")[0]
        return "".join(buf)    
    return _make_line


class TestStride:
    class TestProcess():
        @pytest.mark.parametrize(
             "lines, expected_len",
             [
                 pytest.param(
                     [(1, "", "A", "ALA", "H"),
                      (2, "", "A", "VAL", "E"),
                      (3, "", "B", "GLY", "C"),],
                     3,
                      id='good_data',
                 ),
                 pytest.param(
                     [(1, "", "A", "ALA", "H", True)],
                     0,
                     id='bad_data',
                 ),
                 pytest.param(
                     [],
                     0,
                     id='no_data',
                 )
             ]
            
        )
        def test_process_data_basic(self, make_algorithm, make_line, lines, expected_len):
            alg = make_algorithm(Stride, "stride", None)
            body = "\n".join(make_line(*args) for args in lines)
            algorithm_out = body + "\n"
            arr = alg.process_data(algorithm_out)
            assert len(arr) == expected_len
            assert arr.dtype.names == ("residue_index", "insertion_code", "chain_id", "AA", "SS", "SS_code")
            if expected_len:
                res_idx, ins, chain, aa3, ss_code = lines[0]
                assert arr["residue_index"][0] == res_idx
                assert arr["insertion_code"][0] == (ins[0] if ins else "")
                assert arr["chain_id"][0] == chain
                assert arr["AA"][0] in {"A", "V", "G", "L", "F", "S", "T", "Y", "C", "N", "Q", "D", "E", "K", "R", "H", "I", "M", "P", "W"}
                assert arr["SS_code"][0] == ss_code
                if ss_code == "H":
                    assert arr["SS"][0] == "Helix"
                elif ss_code == "E":
                    assert arr["SS"][0] == "Strand"
                elif ss_code == "C":
                    assert arr["SS"][0] == "Other"
                    
        def test_process_custom_dict(self, make_algorithm, make_line, ss_custom):
            alg = make_algorithm(Stride, "stride", ss_custom)
            line = make_line(1, "", "A", "ALA", "H")  # SS_code=H
            # by default H should be translated as 'Helix', but with custom it has to be 'Other'
            arr = alg.process_data(line + "\n")
            assert len(arr) == 1
            assert arr["SS_code"][0] == "H"
            assert arr["SS"][0] == "Other"
            
        def test_process_data_unknown_code_falls_back_to_other(self, make_algorithm, make_line):
            alg = make_algorithm(Stride, "stride", None)  # default table
            line = make_line(2, " ", "A", "G", "X")  # There is no 'X' in deault table
            arr = alg.process_data(line + "\n")
            assert arr["SS_code"][0] == "X"
            assert arr["SS"][0] == "Other"
            
        def test_custom_translation_not_mutated(self, make_algorithm, default_table_stride):
            """A function that should check whether the table is mutated during the function's execution."""
            mapping = default_table_stride # default table
            alg = make_algorithm(Stride, "stride", mapping)
            _ = alg.SS_TRANSLATION['H'] 
            assert mapping['H'] == 'Helix'
